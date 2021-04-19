import ctypes
import asyncio
import os




class testClass:
    loop = None
    future = None
    loadedLibrary = None
    exampleDll = None
    callback_type = None
    callback_as_cfunc = None

    def finish(self):
        #now in the right c thread and eventloop.
        print("callback in eventloop")
        self.future.set_result(999)

    def trampoline(self):
        #still in the other c thread
        self.loop.call_soon_threadsafe(self.finish)

    def example_callback(self):
        #in another c thread, so we need to do threadsafety stuff
        print("callback has arrived")
        self.trampoline()
        return


    async def register_and_wait(self):
        print("future 1")
        self.loop = asyncio.get_event_loop()
        self.future=self.loop.create_future()

        #now register the callback and wait
        print("future 2")
        self.exampleDll.fnminimalExample(self.callback_as_cfunc, ctypes.c_int(1))

        print("future 3")
        await self.future
        print("future has finished")

    def main(self):
        asyncio.run(self.register_and_wait())

    def __init__(self):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "minimalExample.dll")
        #print(path)
        loadedLibrary = ctypes.cdll.LoadLibrary(path)
        #for easy access
        self.exampleDll = ctypes.cdll.minimalExample
        self.callback_type = ctypes.CFUNCTYPE(None)
        self.callback_as_cfunc = self.callback_type(self.example_callback)


if __name__ == "__main__":
    test = testClass()
    for i in range(0,100000):
        print(i)
        test.main()