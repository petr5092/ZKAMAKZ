# check_maxapi.py
import maxapi.types
import maxapi.utils
import inspect

print("=== Available in maxapi.types ===")
for name, obj in inspect.getmembers(maxapi.types):
    if inspect.isclass(obj):
        print(f"Class: {name}")

print("\n=== Available in maxapi.utils ===")
for name, obj in inspect.getmembers(maxapi.utils):
    if inspect.isclass(obj):
        print(f"Class: {name}")

print("\n=== All available in maxapi.types ===")
for name in dir(maxapi.types):
    print(f"maxapi.types.{name}")

print("\n=== All available in maxapi.utils ===")
for name in dir(maxapi.utils):
    print(f"maxapi.utils.{name}")