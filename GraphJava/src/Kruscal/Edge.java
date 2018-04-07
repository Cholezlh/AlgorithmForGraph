package Kruscal;
public class Edge implements Comparable{  
    public Long i,j;
    public Double w;
    /////////下面可以添加任意多属性
    public Double money;
    
     
    public Edge(Long i,Long j,Double w){  
        this.i=i;  
        this.j=j;  
        this.w=w;  
    }  
      
    public Edge(Long i,Long j,Double w, Double money){  
        this.i=i;  
        this.j=j;  
        this.w=w;  
        this.money = money;
    }
    
  
    @Override  
    public int compareTo(Object o) {  
        Edge to=(Edge)o;  
        if(this.w>to.w) return 1;  
        else if(this.w==to.w) return 0;  
        else return -1;  
          
    }  
    
    
//    @Override  
//    public String toString() {  
//        return "start="+i+"||end="+j+"||w="+w;  
//    }  
}  