# Делает obs.def из экспортов obs.dll (нужен, чтобы lib.exe создал obs.lib).
import sys, pefile
dll, out = sys.argv[1], sys.argv[2]
pe = pefile.PE(dll, fast_load=True)
pe.parse_data_directories([pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_EXPORT"]])
names = sorted({e.name.decode() for e in pe.DIRECTORY_ENTRY_EXPORT.symbols if e.name})
if len(names) < 500:
    sys.exit("obs.dll: слишком мало экспортов (%d)" % len(names))
with open(out, "w") as f:
    f.write("LIBRARY obs.dll\nEXPORTS\n")
    for n in names:
        f.write("    %s\n" % n)
print("obs.def: %d экспортов" % len(names))
