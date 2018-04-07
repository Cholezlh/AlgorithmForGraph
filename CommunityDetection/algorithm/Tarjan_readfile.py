# -*- coding: utf-8 -*-
from collections import namedtuple

""" Context used to implement the algorithm without recursion in @tarjan
    and @tarjan_iter """
TarjanContext = namedtuple('TarjanContext',
                                ['g',           # the graph
                                 'S',           # The main stack of the alg.
                                 'S_set',       # == set(S) for performance
                                 'index',       # { v : <index of v> }
                                 'lowlink',     # { v : <lowlink of v> }
                                 'T',           # stack to replace recursion
                                 'ret'])        # return code

def _tarjan_head(ctx, v):
        """ Used by @tarjan and @tarjan_iter.  This is the head of the
            main iteration """
        ctx.index[v] = len(ctx.index)
        ctx.lowlink[v] = ctx.index[v]
        ctx.S.append(v)
        ctx.S_set.add(v)
        it = iter(ctx.g.get(v, ()))
        ctx.T.append((it,False,v,None))

def _tarjan_body(ctx, it, v):
        """ Used by @tarjan and @tarjan_iter.  This is the body of the
            main iteration """
        for w in it:
                if w not in ctx.index:
                        ctx.T.append((it,True,v,w))
                        _tarjan_head(ctx, w)
                        return
                if w in ctx.S_set:
                        ctx.lowlink[v] = min(ctx.lowlink[v], ctx.index[w])
        if ctx.lowlink[v] == ctx.index[v]:
                scc = []
                w = None
                while v != w:
                        w = ctx.S.pop()
                        scc.append(w)
                        ctx.S_set.remove(w)
                ctx.ret.append(scc)

def tarjan_iter(g):
        """ Returns the strongly connected components of the graph @g
            in a topological order.
                @g is the graph represented as a dictionary
                        { <vertex> : <successors of vertex> }.
            This function does not recurse.  It returns an iterator. """
        ctx = TarjanContext(
                g = g,
                S = [],
                S_set = set(),
                index = {},
                lowlink = {},
                T = [],
                ret = [])
        main_iter = iter(g)
        while True:
                try:
                        v = next(main_iter)
                except StopIteration:
                        return
                if v not in ctx.index:
                        _tarjan_head(ctx, v)
                while ctx.T:
                        it, inside, v, w = ctx.T.pop()
                        if inside:
                                ctx.lowlink[v] = min(ctx.lowlink[w],
                                                        ctx.lowlink[v])
                        _tarjan_body(ctx, it, v)
                        if ctx.ret:
                                assert len(ctx.ret) == 1
                                yield ctx.ret.pop()

def tarjan(g): 
        """ Returns the strongly connected components of the graph @g  非递归版本
            in a topological order.
                @g is the graph represented as a dictionary
                        { <vertex> : <successors of vertex> }.
        
            This function does not recurse. """
        ctx = TarjanContext(
                g = g,
                S = [],
                S_set = set(),
                index = {},
                lowlink = {},
                T = [],
                ret = [])
        main_iter = iter(g)
        while True:
                try:
                        v = next(main_iter)
                except StopIteration:
                        return ctx.ret
                if v not in ctx.index:
                        _tarjan_head(ctx, v)
                while ctx.T:
                        it, inside, v, w = ctx.T.pop()
                        if inside:
                                ctx.lowlink[v] = min(ctx.lowlink[w],
                                                        ctx.lowlink[v])
                        _tarjan_body(ctx, it, v)



if __name__ == '__main__':
#    g = {1: [2,3],
#          2: [4],
#          3: [4,5],
#          4: [1,6],
#          5: [6],
#          6: []}
#    print tarjan(g)
    
    g2 = {}
    with open('../network/scc.txt') as text:  
        for line in text:
            print line
            (src,dst) = line.strip().split('\t')
            if src in g2.keys() and dst in g2.keys():
                g2[src].append(dst)
            elif src in g2.keys():
                g2[dst] = []
                g2[src].append(dst)
            else:
                g2[src] = [dst]
    #print g2
    print tarjan(g2)
                
                
    