from typing import TextIO
import queue
import json

class Queue:
    def __init__(self):
        self.queue = queue.Queue()
    async def write(
        self,
        item :str=None
    ):
        """Write an item to the queue."""
        if hasattr(self, "queue") and self.queue != None and isinstance(self.queue, queue.Queue):  # noqa: E711
            if item == None or isinstance(item, str) == False:  # noqa: E711, E712
                return
            await self.queue.put(
                item=item
            )
    async def read(
        self,
    ):
        """Read and remove one item from the queue."""
        if hasattr(self, "queue") and self.queue != None and isinstance(self.queue, queue.Queue):  # noqa: E711
            if not self.is_empty():
                return await self.queue.get()
    def size(
        self
    ):
        """Return current queue size."""
        if hasattr(self, "queue") and self.queue != None and isinstance(self.queue, queue.Queue):  # noqa: E711
            return self.queue.qsize()
    def is_empty(
        self
    ):
        """Check if the queue is empty."""
        if hasattr(self, "queue") and self.queue != None and isinstance(self.queue, queue.Queue):  # noqa: E711
            return self.queue.empty()
    async def peek(
        self
    ):
        """Peek at the next item without removing it."""
        # No indexing, instead replacing it with snapshot
        # if not self.is_empty():
        #     item = await self.read()
        #     await self.write(
        #         item=item
        #     )
        #     return item
        if not self.is_empty():
            items = await self.snapshot()
            if items != None and isinstance(items, list):  # noqa: E711
                if items.__len__() > 0:
                    return items[0]
    async def drain(
        self
    ):
        """Remove and return all items from the queue."""
        items = []
        while not self.is_empty():
            items.append(await self.read())
        return items
    async def snapshot(
        self
    ):
        """Return a snapshot of the queue contents without removing them."""
        if not self.is_empty():
            items = []
            for _ in range(self.size()):
                item = await self.read()
                items.append(item)
                await self.write(
                    item=item
                )
            return items
    async def clear(
        self
    ):
        """Clear all items in the queue."""
        await self.drain()
    async def dump(
        self,
        fp :TextIO=None
    ):
        """Write queue contents to a file, one per line."""
        if fp == None or isinstance(fp, TextIO) == False:  # noqa: E711, E712
            return
        fp.write(
            s=await self.dumps()
        )
    async def dumps(
        self
    ):
        """Return queue contents as a string with one item per line."""
        return "\n".join(str(item) for item in await self.snapshot())
    async def load(
        self,
        fp :TextIO=None
    ):
        """Load items into the queue from a text file (one item per line)."""
        if fp == None or isinstance(fp, TextIO) == False:  # noqa: E711, E712
            return
        for line in fp.readlines():
            await self.write(
                item=line.strip()
            )
    async def loads(
        self,
        data :str=None
    ):
        """Load items into the queue from a string (one item per line)."""
        if data == None or isinstance(data, str) == False:  # noqa: E711, E712
            return
        for line in data.splitlines():
            await self.write(
                item=line.strip()
            ) 
    async def dump_snapshot_json(
        self,
        fp :TextIO=None,
        indent :int=None
    ):
        """Write the queue to a file in JSON format."""
        if fp == None or isinstance(fp, TextIO) == False:  # noqa: E711, E712
            return
        json.dump(
            fp=fp,
            obj=await self.snapshot(),
            indent=indent
        )
    async def dumps_snapshot_json(
        self,
        indent :int=None
    ):
        """Return the queue as a JSON string."""
        return json.dumps(
            obj=await self.snapshot(),
            indent=indent
        )
    async def load_snapshot_json(
        self,
        fp: TextIO = None
    ):
        """Load items into the queue from a JSON file (expects a list)."""
        if fp == None or isinstance(fp, TextIO) == False:  # noqa: E711, E712
            return
        data = json.load(
            fp=fp
        )
        if data == None or isinstance(data, list) == False:  # noqa: E711, E712
            return
        for item in data:
            await self.write(
                item=data
            )
    async def loads_snapshot_json(
        self,
        data :str=None
    ):
        """Load items into the queue from a JSON string (expects a list)."""
        for item in json.loads(
            s=data
        ):
            await self.write(
                item=data
            )
    async def write_bulk(
        self,
        items :list=None
    ):
        """Write multiple items into the queue."""
        if items == None or isinstance(items, list) == False:  # noqa: E711, E712
            return
        for item in items:
            await self.write(
                item=item
            )
    async def read_bulk(
        self, 
        n :int=None
    ):
        """Read up to n items from the queue."""
        if n == None or isinstance(n, int) == False:  # noqa: E711, E712
            return
        results = []
        for _ in range(min(n, self.size())):
            results.append(await self.read())
        return results