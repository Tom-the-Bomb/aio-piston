# Aio-piston
This is an unoffical Api wrapper for the [piston code execution engine](https://emkc.org/api/v2/piston/)

**Examples**
```py
import aio_piston
import asyncio

async def main():
    async with await aio_piston.Piston() as piston:
        out = await piston.execute('print("hello world")', language="python")
        #execute the code
        out2 = await piston.execute('print(input("what is your name"))', language="python", inputs="bob")
        return out, out2

    #*OR* without a context manager
    piston = await aio_piston.Piston()
    ...
    #do stuff
    ...
    #at the end
    await piston.close()

out, out2 = asyncio.run(main())

print(str(out))
#full output
print(vars(out).keys())
#all the attributes of the response class
```
