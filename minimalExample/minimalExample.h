// The following ifdef block is the standard way of creating macros which make exporting
// from a DLL simpler. All files within this DLL are compiled with the MINIMALEXAMPLE_EXPORTS
// symbol defined on the command line. This symbol should not be defined on any project
// that uses this DLL. This way any other project whose source files include this file see
// MINIMALEXAMPLE_API functions as being imported from a DLL, whereas this DLL sees symbols
// defined with this macro as being exported.
#pragma once
#ifdef MINIMALEXAMPLE_EXPORTS
#define MINIMALEXAMPLE_API extern "C" __declspec(dllexport)
#else
#define MINIMALEXAMPLE_API __declspec(dllimport)
#endif

MINIMALEXAMPLE_API int fnminimalExample(void* callback_to_python, int mode);

