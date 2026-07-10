from collections import deque


def bfs(grid, start, goal):

    rows = len(grid)
    cols = len(grid[0])

    queue = deque([start])

    visited = {start}

    parent = {}

    directions = [
        (-1,0),
        (1,0),
        (0,-1),
        (0,1)
    ]

    while queue:

        r,c = queue.popleft()

        if (r,c)==goal:

            path=[]

            cur=goal

            while cur!=start:

                path.append(cur)

                cur=parent[cur]

            path.append(start)

            path.reverse()

            return path

        for dr,dc in directions:

            nr=r+dr
            nc=c+dc

            if not(0<=nr<rows and 0<=nc<cols):
                continue

            if grid[nr][nc]=="#":
                continue

            if (nr,nc) in visited:
                continue

            visited.add((nr,nc))

            parent[(nr,nc)]=(r,c)

            queue.append((nr,nc))

    return None


def is_reachable(grid,start,goal):

    return bfs(grid,start,goal) is not None


def bfs_steps(grid,start,goal):

    path=bfs(grid,start,goal)

    if path is None:
        return None

    return len(path)-1