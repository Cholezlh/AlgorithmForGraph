package StronglyConnectedComponent;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Stack;


public class Tarjan {
	private int numOfNode;
	private List< ArrayList<Integer> > graph;//图
	private List< ArrayList<Integer> > result;//保存极大强连通图
	private boolean[] inStack;//节点是否在栈内，因为在stack中寻找一个节点不方便。这种方式查找快
	private Stack<Integer> stack;
	private int[] dfn;
	private int[] low;
	private int time;//
	
	public Tarjan(List< ArrayList<Integer> > graph,int numOfNode){
		this.graph = graph;
		this.numOfNode = numOfNode;
		this.inStack = new boolean[numOfNode];
		this.stack = new Stack<Integer>();
		dfn = new int[numOfNode];
		low = new int[numOfNode];
		Arrays.fill(dfn, -1);//将dfn所有元素都置为-1，其中dfn[i]=-1代表i还有没被访问过。
		Arrays.fill(low, -1);
		result = new ArrayList<ArrayList<Integer>>();
	}
	
	public List< ArrayList<Integer> > run(){
		for(int i=0;i<numOfNode;i++){
			if(dfn[i]==-1){
				tarjan(i);
			}
		}
		return result;
	}
	
	public void tarjan(int current){
		dfn[current]=low[current]=time++;
		inStack[current]=true;
		stack.push(current);
		
		for(int i=0;i<graph.get(current).size();i++){
			int next = graph.get(current).get(i);
			if(dfn[next]==-1){//-1代表没有被访问
				tarjan(next);
				low[current]=Math.min(low[current], low[next]);
			}else if(inStack[next]){
				low[current]=Math.min(low[current], dfn[next]);
			}
		}
		
		if(low[current]==dfn[current]){
			ArrayList<Integer> temp =new ArrayList<Integer>();
			int j = -1;
			while(current!=j){
				j = stack.pop();
				inStack[j]=false;
				temp.add(j);
			}
			result.add(temp);			
		}
	}
	
}


