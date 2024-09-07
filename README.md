
# Aio-piston

This is a simple, unoffical python asynchronous API wrapper for the [piston code execution engine](https://emkc.org/api/v2/piston/)

## Example

```py
...
# assuming you are already inside an async environment and have already imported everything
# to instantiate:
#
# - It is recommended to have a global class if you are going to run `execute()` more than 1 time throughout the program
#
# - Alternatively you can use the async context manager if it's a one time use:
#   `async with aio_piston.Piston() as piston: ...`
piston = aio_piston.Piston() # pass in Optional 'loop' and 'session' kwargs etc.

# to execute
output = await piston.execute(
    "print('')",
    language="python"
) # you can pass in additional optional kwargs if needed

print(str(output)) # returns the full output, returns the .output attr
print(output.stdout) # returns the stdout only

print(vars(output).keys())
# all the attributes of the response class: .language, .stdout etc.
```

---
