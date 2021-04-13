// minimalExample.cpp : Defines the exported functions for the DLL.
//

#include "pch.h"
#include "framework.h"
#include <Windows.h>
#include "minimalExample.h"

HANDLE callback_thread;
DWORD threadID;

typedef void (*CallbackFct)();

DWORD WINAPI eventuallyCallback(LPVOID lpParam) {
  Sleep(2000);
  auto callback=reinterpret_cast<CallbackFct>(lpParam);
  callback();
  return 0;
}

DWORD WINAPI immediateCallback(LPVOID lpParam) {
  auto callback = reinterpret_cast<CallbackFct>(lpParam);
  callback();
  return 0;
}


// wait 2 seconds then perform the callback
MINIMALEXAMPLE_API int fnminimalExample(void* callback_to_python, int mode)
{
  if (mode == 0) {
    callback_thread = CreateThread(
      NULL,
      0,
      eventuallyCallback,
      callback_to_python,
      0,
      &threadID
    );
  }
  else {
    callback_thread = CreateThread(
      NULL,
      0,
      immediateCallback,
      callback_to_python,
      0,
      &threadID
    );
  }
  WaitForSingleObject(callback_thread, 0);

  return 0;
}
