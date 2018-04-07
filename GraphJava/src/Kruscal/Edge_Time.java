package Kruscal;
public class Edge_Time implements Comparable{  
    public Long i,j;
    public Double w;
    /////////下面可以添加任意多属性
    public Double money;
    public Long time;
    
     
    public Edge_Time(Long i,Long j,Double w){  
        this.i=i;  
        this.j=j;  
        this.w=w;  
    }  
      
    public Edge_Time(Long i,Long j, Double w, Double money, Long time){  
        this.i=i;  
        this.j=j;
        this.w=w;  
        this.money=money;
        this.time=time;
    }
    
  
    @Override  
    public int compareTo(Object o) {  
        Edge_Time to=(Edge_Time)o;  
        if(this.w>to.w) return 1;  
        else if(this.w==to.w) return 0;  
        else return -1;  
          
    }  
    
    
//    @Override  
//    public String toString() {  
//        return "start="+i+"||end="+j+"||w="+w;  
//    }  
}  