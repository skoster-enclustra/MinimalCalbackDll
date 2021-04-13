import ctypes
import asyncio
import os




class testClass:
    loop = None
    future = None
    exampleDll = None


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
        self.loop = asyncio.get_event_loop()
        self.future=self.loop.create_future()

        callback_type = ctypes.CFUNCTYPE(None)
        callback_as_cfunc = callback_type(self.example_callback)

        #now register the callback and wait
        self.exampleDll.fnminimalExample(callback_as_cfunc, ctypes.c_int(1))

        await self.future
        print("future has finished")

    def main(self):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "minimalExample.dll")
        #print(path)
        ctypes.cdll.LoadLibrary(path)
        #for easy access
        self.exampleDll = ctypes.cdll.minimalExample

        asyncio.run(self.register_and_wait())


if __name__ == "__main__":
    for i in range(0,100000):
        print(i)
        test = testClass()
        test.main()