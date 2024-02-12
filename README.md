# Avoid All Eyes
A Python-based tool designed to attempt to hide processes from task managers.

# FAQ
### Why?
I encountered this on a random forum that is well over 15 years old. The method logically should still work. It is based on DKOM (Direct Kernel Object Manipulation).

### What exactly is DKOM?
DKOM stands for Direct Kernel Object Manipulation. Each process has an `EPROCESS` struct (which isn't officially documented) in the kernel's memory. This structure contains information such as `PID`, `exe name`, and various other details. The struct member that interests us is `LIST_ENTRY ActiveProcessLinks`. The `Flink` member of this struct points to the next entry (process) in the doubly-linked list, while the `Blink` member points to the previous entry (process).

---

![diagram1](http://i159.photobucket.com/albums/t141/sovietweasel/plist.jpg)

Based on the user's claim on the forum, we can conclude that all we would logically need to do is disconnect it from the doubly-linked list. What we need to do is set the `Flink` of the process preceding the process we want to hide to the `Flink` of the process we're hiding.

**Note: I included the original source of the poster's version; my version was re-written in Python, while theirs is in C.**

Hidden Process Diagram:
---
![diagram2](http://i159.photobucket.com/albums/t141/sovietweasel/plist2.jpg)

I should probably mention that if you want to reverse this process, you should restore the original `Blink` and `Flink` pointers. You can achieve this by saving the original pointer contents to a storage medium, such as a JSON file, and then restoring based on that.

--- 

```py
p_list_procs = ListEntry.from_address(self.e_process_address + self.u_flink_offset)
p_list_procs.Blink, p_list_procs.Flink = (
  ctypes.c_void_p(self.original_pointers["Blink"]),
  ctypes.c_void_p(self.original_pointers["Flink"]),
)
```
