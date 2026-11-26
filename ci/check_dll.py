# Проверка собранной DLL: экспорты модуля OBS и наличие новых имён клавиш из патча.
import sys, pefile
p = sys.argv[1]
pe = pefile.PE(p, fast_load=True)
pe.parse_data_directories([pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_EXPORT"]])
exp = {e.name.decode() for e in pe.DIRECTORY_ENTRY_EXPORT.symbols if e.name}
data = open(p, "rb").read()
bad = []
for n in ("obs_module_load", "obs_module_ver"):
    if n not in exp: bad.append("нет экспорта " + n)
for k in (b"esc", b"lalt", b"ralt", b"lwin", b"backspace", b"enter", b"num/"):
    if (b"\x00" + k + b"\x00") not in data: bad.append("в DLL нет имени клавиши " + k.decode())
if pe.FILE_HEADER.Machine != 0x8664: bad.append("DLL не x64")
print("DLL:", p, len(data), "байт")
print("ПРОВЕРКА DLL: OK" if not bad else "ПРОВЕРКА DLL: ОШИБКИ\n" + "\n".join(bad))
sys.exit(1 if bad else 0)
