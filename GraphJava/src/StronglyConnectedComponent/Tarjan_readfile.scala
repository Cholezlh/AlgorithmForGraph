package StronglyConnectedComponent

import  scala.collection.mutable.{Buffer,Set,Map}


object Tarjan_readfile{
    def main(args: Array[String]) {

    
    val result = tarjan_scc(Map(
      1 -> List(2,3),    2 -> List(4), 3 -> List(4,5),
      4 -> List(1,6), 5 -> List(6),    6 -> Nil
    ))
    
    println(result)
    
   }
    

   

def tarjan_scc(g: Map[Int, List[Int]])= {
  val st = Buffer.empty[Int]
  val st_set = Set.empty[Int]
  val i = Map.empty[Int, Int]
  val lowl = Map.empty[Int, Int]
  val result = Buffer.empty[Buffer[Int]]

  def visit(v: Int): Unit = {
    i(v) = i.size
    lowl(v) = i(v)
    st += v
    st_set += v

    for (w <- g(v)) {
      if (!i.contains(w)) {
        visit(w)
        lowl(v) = math.min(lowl(w), lowl(v))
      } else if (st_set(w)) {
        lowl(v) = math.min(lowl(v), i(w))
      }
    }

    if (lowl(v) == i(v)) {
      val scc = Buffer.empty[Int]
      var w = -1

      while(v != w) {
        w = st.remove(st.size - 1)
        scc += w
        st_set -= w
      }

      if(scc.size>1)
        result += scc
    }
  }

  for (v <- g.keys) 
    if (!i.contains(v)) 
      visit(v)
     
  result
}



}