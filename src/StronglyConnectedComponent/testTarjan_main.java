package StronglyConnectedComponent;


import java.util.ArrayList;
import java.util.List;
import java.util.Stack;


public class testTarjan_main {
	public static void main(String[] args) {
                //创建图
		int numOfNode = 6;
		List< ArrayList<Integer> > graph = new ArrayList<ArrayList<Integer>>();
		for(int i=0;i<numOfNode;i++){
			graph.add(new ArrayList<Integer>());
		}
		graph.get(0).add(1);
		graph.get(0).add(2);
		graph.get(1).add(3);
		graph.get(2).add(3);
		graph.get(2).add(4);
		graph.get(3).add(0);
		graph.get(3).add(5);
		graph.get(4).add(5);
		//调用Tarjan算法求极大连通子图
		Tarjan t = new Tarjan(graph, numOfNode);
		List< ArrayList<Integer> > result = t.run();
                //打印结果
		for(int i=0;i<result.size();i++){
			for(int j=0;j<result.get(i).size();j++){
				System.out.print(result.get(i).get(j)+" ");
			}
			System.out.println();
		}
		
	}
}

