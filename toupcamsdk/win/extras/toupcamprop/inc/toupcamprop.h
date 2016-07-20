#ifndef __toupcamprop_h__
#define __toupcamprop_h__

#ifdef __cplusplus
extern "C" {
#endif

#pragma pack(push, 8)
#ifdef TOUPCAMPROP_EXPORTS
#define toupcamprop_ports(x)    __declspec(dllexport)   x   __stdcall
#else
#define toupcamprop_ports(x)    __declspec(dllimport)   x   __stdcall
#pragma comment(lib, "toupcamprop.lib")
#include "toupcam.h"
#endif

toupcamprop_ports(void)     toupcamprop_propertysheet(HToupCam h, HWND hParent);
toupcamprop_ports(void)     toupcamprop_propertysheet_phd2(HToupCam h, HWND hParent);

#ifdef _WIN32
#pragma pack(pop)
#endif

#ifdef __cplusplus
}
#endif

#endif
