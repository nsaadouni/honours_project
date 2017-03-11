/*
 * A significant part of code is taken from the 'libpcscspy' of OpenSc project: https://github.com/LudovicRousseau/PCSC/blob/master/src/spy/libpcscspy.c
 * However, the implementation of main functionality, tracing inner functions of Athena card driver, is original.
 *
 */


#include <dlfcn.h>
#include <execinfo.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "misc.h"
#include <winscard.h>

#define BT_BUF_SIZE 100

/* function prototypes */

#define p_SCardEstablishContext(fct) LONG(fct)(DWORD dwScope, LPCVOID pvReserved1, LPCVOID pvReserved2, LPSCARDCONTEXT phContext)

#define p_SCardReleaseContext(fct) LONG(fct)(SCARDCONTEXT hContext)

#define p_SCardIsValidContext(fct) LONG(fct) (SCARDCONTEXT hContext)

#define p_SCardConnect(fct) LONG(fct) (SCARDCONTEXT hContext, LPCSTR szReader, DWORD dwShareMode, DWORD dwPreferredProtocols, LPSCARDHANDLE phCard, LPDWORD pdwActiveProtocol)

#define p_SCardReconnect(fct) LONG(fct) (SCARDHANDLE hCard, DWORD dwShareMode, DWORD dwPreferredProtocols, DWORD dwInitialization, LPDWORD pdwActiveProtocol)

#define p_SCardDisconnect(fct) LONG(fct) (SCARDHANDLE hCard, DWORD dwDisposition)

#define p_SCardBeginTransaction(fct) LONG(fct) (SCARDHANDLE hCard)

#define p_SCardEndTransaction(fct) LONG(fct) (SCARDHANDLE hCard, DWORD dwDisposition)

#define p_SCardStatus(fct) LONG(fct) (SCARDHANDLE hCard, LPSTR mszReaderName, LPDWORD pcchReaderLen, LPDWORD pdwState, LPDWORD pdwProtocol, LPBYTE pbAtr, LPDWORD pcbAtrLen)

#define p_SCardGetStatusChange(fct) LONG(fct) (SCARDCONTEXT hContext, DWORD dwTimeout, LPSCARD_READERSTATE rgReaderStates, DWORD cReaders)

#define p_SCardControl(fct) LONG(fct) (SCARDHANDLE hCard, DWORD dwControlCode, LPCVOID pbSendBuffer, DWORD cbSendLength, LPVOID pbRecvBuffer, DWORD cbRecvLength, LPDWORD lpBytesReturned)

#define p_SCardTransmit(fct) LONG(fct) (SCARDHANDLE hCard, const SCARD_IO_REQUEST * pioSendPci, LPCBYTE pbSendBuffer, DWORD cbSendLength, SCARD_IO_REQUEST * pioRecvPci, LPBYTE pbRecvBuffer, LPDWORD pcbRecvLength)

#define p_SCardListReaderGroups(fct) LONG(fct) (SCARDCONTEXT hContext, LPSTR mszGroups, LPDWORD pcchGroups)

#define p_SCardListReaders(fct) LONG(fct) (SCARDCONTEXT hContext, LPCSTR mszGroups, LPSTR mszReaders, LPDWORD pcchReaders)

#define p_SCardFreeMemory(fct) LONG(fct) (SCARDCONTEXT hContext, LPCVOID pvMem)

#define p_SCardCancel(fct) LONG(fct) (SCARDCONTEXT hContext)

#define p_SCardGetAttrib(fct) LONG(fct) (SCARDHANDLE hCard, DWORD dwAttrId, LPBYTE pbAttr, LPDWORD pcbAttrLen)

#define p_SCardSetAttrib(fct) LONG(fct) (SCARDHANDLE hCard, DWORD dwAttrId, LPCBYTE pbAttr, DWORD cbAttrLen)

#define p_pcsc_stringify_error(fct) char *(fct)(const LONG pcscError)

/* fake function to just return en error code */
static LONG internal_error(void)
{
  return SCARD_F_INTERNAL_ERROR;
}

static const char * internal_stringify_error(void)
{
  return "No spy pcsc_stringify_error() function";
}

/* contains pointers to real functions */
static struct
{
  p_SCardEstablishContext(*SCardEstablishContext);
  p_SCardReleaseContext(*SCardReleaseContext);
  p_SCardIsValidContext(*SCardIsValidContext);
  p_SCardConnect(*SCardConnect);
  p_SCardReconnect(*SCardReconnect);
  p_SCardDisconnect(*SCardDisconnect);
  p_SCardBeginTransaction(*SCardBeginTransaction);
  p_SCardEndTransaction(*SCardEndTransaction);
  p_SCardStatus(*SCardStatus);
  p_SCardGetStatusChange(*SCardGetStatusChange);
  p_SCardControl(*SCardControl);
  p_SCardTransmit(*SCardTransmit);
  p_SCardListReaderGroups(*SCardListReaderGroups);
  p_SCardListReaders(*SCardListReaders);
  p_SCardFreeMemory(*SCardFreeMemory);
  p_SCardCancel(*SCardCancel);
  p_SCardGetAttrib(*SCardGetAttrib);
  p_SCardSetAttrib(*SCardSetAttrib);
  p_pcsc_stringify_error(*pcsc_stringify_error);
} spy = {
  /* initialized with the fake internal_error() function */
  .SCardEstablishContext = (p_SCardEstablishContext(*))internal_error,
  .SCardReleaseContext = (p_SCardReleaseContext(*))internal_error,
  .SCardIsValidContext = (p_SCardIsValidContext(*))internal_error,
  .SCardConnect = (p_SCardConnect(*))internal_error,
  .SCardReconnect = (p_SCardReconnect(*))internal_error,
  .SCardDisconnect = (p_SCardDisconnect(*))internal_error,
  .SCardBeginTransaction = (p_SCardBeginTransaction(*))internal_error,
  .SCardEndTransaction = (p_SCardEndTransaction(*))internal_error,
  .SCardStatus = (p_SCardStatus(*))internal_error,
  .SCardGetStatusChange = (p_SCardGetStatusChange(*))internal_error,
  .SCardControl = (p_SCardControl(*))internal_error,
  .SCardTransmit = (p_SCardTransmit(*))internal_error,
  .SCardListReaderGroups = (p_SCardListReaderGroups(*))internal_error,
  .SCardListReaders = (p_SCardListReaders(*))internal_error,
  .SCardFreeMemory = (p_SCardFreeMemory(*))internal_error,
  .SCardCancel = (p_SCardCancel(*))internal_error,
  .SCardGetAttrib = (p_SCardGetAttrib(*))internal_error,
  .SCardSetAttrib = (p_SCardSetAttrib(*))internal_error,
  .pcsc_stringify_error = (p_pcsc_stringify_error(*))internal_stringify_error
};

static void *Lib_handle = NULL;

void fprint_hex(FILE* stream, const char *s, const int length)
{
  for(int i = length; i > 0; i--)
    fprintf(stream, "%02hhx ", (unsigned char) *s++);
}

static LONG load_lib(void)
{

#define LIBPCSC "/lib/x86_64-linux-gnu/libpcsclite.so.1.0.0"

  Lib_handle = dlopen(LIBPCSC, RTLD_LAZY);

#define get_symbol(s) do { spy.s = dlsym(Lib_handle, #s); if (NULL == spy.s) { return SCARD_F_INTERNAL_ERROR; } } while (0)

  if (SCardEstablishContext == dlsym(Lib_handle, "SCardEstablishContext"))
    return SCARD_F_INTERNAL_ERROR;

  get_symbol(SCardEstablishContext);
  get_symbol(SCardReleaseContext);
  get_symbol(SCardIsValidContext);
  get_symbol(SCardConnect);
  get_symbol(SCardReconnect);
  get_symbol(SCardDisconnect);
  get_symbol(SCardBeginTransaction);
  get_symbol(SCardEndTransaction);
  get_symbol(SCardStatus);
  get_symbol(SCardGetStatusChange);
  get_symbol(SCardControl);
  get_symbol(SCardTransmit);
  get_symbol(SCardListReaderGroups);
  get_symbol(SCardListReaders);
  get_symbol(SCardFreeMemory);
  get_symbol(SCardCancel);
  get_symbol(SCardGetAttrib);
  get_symbol(SCardSetAttrib);
  get_symbol(pcsc_stringify_error);

  return SCARD_S_SUCCESS;
}

/* exported functions */
PCSC_API p_SCardEstablishContext(SCardEstablishContext)
{
  LONG rv;
  static int init = 0;

  if (!init)
    {
      init = 1;

      /* load the real library */
      rv = load_lib();
      if (rv != SCARD_S_SUCCESS)
        return rv;
    }
  rv = spy.SCardEstablishContext(dwScope, pvReserved1, pvReserved2,
		                 phContext);

  return rv;
}

PCSC_API p_SCardReleaseContext(SCardReleaseContext)
{
  LONG rv;

  rv = spy.SCardReleaseContext(hContext);
  return rv;
}

PCSC_API p_SCardIsValidContext(SCardIsValidContext)
{
  LONG rv;

  rv = spy.SCardIsValidContext(hContext);
  return rv;
}

PCSC_API p_SCardConnect(SCardConnect)
{
  LONG rv;

  rv = spy.SCardConnect(hContext, szReader, dwShareMode,
                        dwPreferredProtocols, phCard, pdwActiveProtocol);
  return rv;
}

PCSC_API p_SCardReconnect(SCardReconnect)
{
  LONG rv;

  rv = spy.SCardReconnect(hCard, dwShareMode, dwPreferredProtocols,
		          dwInitialization, pdwActiveProtocol);

  return rv;
}

PCSC_API p_SCardDisconnect(SCardDisconnect)
{
  LONG rv;

  rv = spy.SCardDisconnect(hCard, dwDisposition);

  return rv;
}

PCSC_API p_SCardBeginTransaction(SCardBeginTransaction)
{
  LONG rv;

  rv = spy.SCardBeginTransaction(hCard);

  return rv;
}

PCSC_API p_SCardEndTransaction(SCardEndTransaction)
{
  LONG rv;

  rv = spy.SCardEndTransaction(hCard, dwDisposition);

  return rv;
}

PCSC_API p_SCardStatus(SCardStatus)
{
  LONG rv;

  rv = spy.SCardStatus(hCard, mszReaderName, pcchReaderLen, pdwState,
                       pdwProtocol, pbAtr, pcbAtrLen);

  return rv;
}

PCSC_API p_SCardGetStatusChange(SCardGetStatusChange)
{
  LONG rv;

  rv = spy.SCardGetStatusChange(hContext, dwTimeout, rgReaderStates,
                                cReaders);

  return rv;
}

PCSC_API p_SCardControl(SCardControl)
{
  LONG rv;

  rv = spy.SCardControl(hCard, dwControlCode, pbSendBuffer, cbSendLength,
                        pbRecvBuffer, cbRecvLength, lpBytesReturned);

  return rv;
}

PCSC_API p_SCardTransmit(SCardTransmit)
{
  LONG rv;
  int j, nptrs;
  void *buffer[BT_BUF_SIZE];
  char **strings;

  rv = spy.SCardTransmit(hCard, pioSendPci, pbSendBuffer, cbSendLength,
                         pioRecvPci, pbRecvBuffer, pcbRecvLength);

  nptrs = backtrace(buffer, BT_BUF_SIZE);
  //printf("backtrace() returned %d addresses\n", nptrs);

  /* The call backtrace_symbols_fd(buffer, nptrs, STDOUT_FILENO)
     would produce similar output to the following: */

  strings = backtrace_symbols(buffer, nptrs);
  if (strings == NULL) 
    {
      perror("backtrace_symbols");
      exit(EXIT_FAILURE);
    }

  for (j = 0; j < nptrs; j++)
    {
      char *token;
      int found;

#define TARGET "LASERCard"

      strtok(strings[j], "(");
      token = strtok(NULL, "(");
      token = strtok(token, "+");     
      found = !strncmp(token, TARGET, strlen(TARGET));

      if (found)
        {
          fprintf(stdout, "%s\n", token);
          break;
        }
    }
  free(strings);
  
  fprintf(stdout, "APDU: ");
  fprint_hex(stdout, (const char *) pbSendBuffer, cbSendLength);
  fprintf(stdout, "\nSW: ");
  fprint_hex(stdout, (const char *) pbRecvBuffer, *pcbRecvLength);
  fprintf(stdout, "\n\n");

  return rv;
}

PCSC_API p_SCardListReaderGroups(SCardListReaderGroups)
{
  LONG rv;

  rv = spy.SCardListReaderGroups(hContext, mszGroups, pcchGroups);

  return rv;
}

PCSC_API p_SCardListReaders(SCardListReaders)
{
  LONG rv;

  rv = spy.SCardListReaders(hContext, mszGroups, mszReaders, pcchReaders);

  return rv;
}

PCSC_API p_SCardFreeMemory(SCardFreeMemory)
{
  LONG rv;

  rv = spy.SCardFreeMemory(hContext, pvMem);

  return rv;
}

PCSC_API p_SCardCancel(SCardCancel)
{
  LONG rv;

  rv = spy.SCardCancel(hContext);

  return rv;
}

PCSC_API p_SCardGetAttrib(SCardGetAttrib)
{
  LONG rv;

  rv = spy.SCardGetAttrib(hCard, dwAttrId, pbAttr, pcbAttrLen);

  return rv;
}

PCSC_API p_SCardSetAttrib(SCardSetAttrib)
{
  LONG rv;

  rv = spy.SCardSetAttrib(hCard, dwAttrId, pbAttr, cbAttrLen);

  return rv;
}

PCSC_API p_pcsc_stringify_error(pcsc_stringify_error)
{
  return spy.pcsc_stringify_error(pcscError);
}

PCSC_API const SCARD_IO_REQUEST g_rgSCardT0Pci = {
  SCARD_PROTOCOL_T0, sizeof(SCARD_IO_REQUEST) 
};
PCSC_API const SCARD_IO_REQUEST g_rgSCardT1Pci = {
  SCARD_PROTOCOL_T1, sizeof(SCARD_IO_REQUEST)
};
PCSC_API const SCARD_IO_REQUEST g_rgSCardRawPci = {
  SCARD_PROTOCOL_RAW, sizeof(SCARD_IO_REQUEST)
};
