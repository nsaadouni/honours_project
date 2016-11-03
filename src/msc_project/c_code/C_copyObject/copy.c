/*
 * Compiling this code requires the Athena card driver file: libASEP11.so
 * 
 */


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "pkcs11.h"

#define CRYPTOKI_COMPAT 1
#define PIN "12345"

void 
check_return_value(CK_RV rv, const char *message)
{
  if (rv != CKR_OK) {
    fprintf(stderr, "Error at %s: %u\n", message, (unsigned int) rv);
    exit(EXIT_FAILURE);
  }
}

void
initialize()
{
  CK_RV rv;

  rv =  C_Initialize(NULL);
  check_return_value(rv, "initialize");
}

CK_SLOT_ID 
get_slot()
{
  CK_RV rv;
  CK_SLOT_ID slot_id;
  CK_ULONG slot_count = 10;
  CK_SLOT_ID *slot_ids = malloc(sizeof(CK_SLOT_ID) * slot_count);

  rv = C_GetSlotList(CK_TRUE, slot_ids, &slot_count);
  check_return_value(rv, "get slot list");
  if (slot_count < 1) 
    {
      fprintf(stderr, "Error; could not find any slots\n");
      exit(1);
    }
  slot_id = slot_ids[0];
  free(slot_ids);

  return slot_id;
}

CK_SESSION_HANDLE 
start_session(CK_SLOT_ID slot_id)
{
  CK_RV rv;
  CK_SESSION_HANDLE session;

  rv = C_OpenSession(slot_id, CKF_SERIAL_SESSION | CKF_RW_SESSION, 
                     NULL, NULL, &session);
  check_return_value(rv, "open session");

  return session;
}

void 
login(CK_SESSION_HANDLE session, CK_BYTE *pin)
{
  CK_RV rv;

  if (pin) 
    {
      rv = C_Login(session, CKU_USER, pin, strlen((char *) pin));
      check_return_value(rv, "log in");
    }
}

void 
logout(CK_SESSION_HANDLE session)
{
  CK_RV rv;

  rv = C_Logout(session);
  if (rv != CKR_USER_NOT_LOGGED_IN) 
    check_return_value(rv, "log out");
}

void 
end_session(CK_SESSION_HANDLE session)
{
  CK_RV rv;

  rv = C_CloseSession(session);
  check_return_value(rv, "close session");
}

void 
finalize()
{
  C_Finalize(NULL);
}

CK_OBJECT_HANDLE 
find_key(CK_SESSION_HANDLE session, CK_OBJECT_CLASS class, CK_BYTE *label)
{
    CK_RV rv;
    CK_ATTRIBUTE template[] = {
        { CKA_CLASS, &class, sizeof(class) },
        { CKA_LABEL, label, sizeof(label) }
    };
    CK_ULONG objectCount;
    CK_OBJECT_HANDLE object;

    rv = C_FindObjectsInit(session, template, 1);
    check_return_value(rv, "Find objects init");

    rv = C_FindObjects(session, &object, 1, &objectCount);
    check_return_value(rv, "Find first object");

    while (objectCount > 0) {
        rv = C_FindObjects(session, &object, 1, &objectCount);
        check_return_value(rv, "Find other objects");
    }

    rv = C_FindObjectsFinal(session);
    check_return_value(rv, "Find objects final");

    return object;
}

void
copy_key(CK_SESSION_HANDLE session, CK_OBJECT_HANDLE key, 
         CK_BYTE *label)
{
    CK_OBJECT_HANDLE new_key;
    CK_BBOOL false = CK_FALSE;
    CK_ATTRIBUTE template[] = {
        {CKA_LABEL, label, sizeof(label)},
        {CKA_PRIVATE, &false, sizeof(false)}
    };
    CK_RV rv;

    rv = C_CopyObject(session, key, template, 2, &new_key);
    check_return_value(rv, "copy key object");
}

int 
main(int argc, char **argv)
{
  CK_SLOT_ID slot;
  CK_SESSION_HANDLE session;
  CK_OBJECT_HANDLE key;

  initialize();
  slot = get_slot();
  session = start_session(slot);
  login(session, (CK_BYTE *) PIN);

  key = find_key(session, CKO_SECRET_KEY, "Hades");
  copy_key(session, key, "Hades_copy");

  logout(session);
  end_session(session);
  finalize();

  return 0;
}
