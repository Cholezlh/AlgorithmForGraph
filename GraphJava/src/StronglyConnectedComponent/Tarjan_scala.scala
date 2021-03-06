package StronglyConnectedComponent

import  scala.collection.mutable.{Buffer,Set,Map}


object Tarjan_scala{
  

    def main(args: Array[String]) {

//    tarjan_scc(Map(
//      1 -> List(2),    2 -> List(1, 5), 3 -> List(4),
//      4 -> List(3, 5), 5 -> List(6),    6 -> List(7),
//      7 -> List(8),    8 -> List(6, 9), 9 -> Nil
//    ))
//    
//    //结果： ArrayBuffer(ArrayBuffer(9), ArrayBuffer(7, 6, 8), ArrayBuffer(5), ArrayBuffer(1, 2), ArrayBuffer(3, 4))
    
    val a = tarjan_anyType(Map(
      1L -> List(2L,3L),  2L -> List(4L), 3L -> List(4L,5L),
      4L -> List(1L,6L), 5L -> List(6L),    6L -> Nil
    ))
    
    println(a)
    println("Done")
    //ArrayBuffer(ArrayBuffer(6), ArrayBuffer(5), ArrayBuffer(3, 1, 4, 2))
    
   }
    


def tarjan_scc(g: Map[Int, List[Int]])= {
  val st = Buffer.empty[Int]
  val st_set = Set.empty[Int]
  val i = Map.empty[Int, Int]
  val lowl = Map.empty[Int, Int]
  val rt = Buffer.empty[Buffer[Int]]

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

      rt += scc
    }
  }

  for (v <- g.keys) 
    if (!i.contains(v)) 
      visit(v)
   
  println(rt)
}


def tarjan_anyType[TP](g: Map[TP, List[TP]])= {
  val stack = collection.mutable.Stack[TP]() 
  val index = Map.empty[TP, Int]
  val lowl = Map.empty[TP, Int]
  val result = Buffer.empty[Buffer[TP]]
  var time = 0;

  def visit(v: TP): Unit = {
    index(v) = time
    lowl(v) = time
    time =time+1
    stack.push(v)
  

    for (w <- g(v)) {
      if (!index.contains(w)) {
        visit(w)
        lowl(v) = math.min(lowl(w), lowl(v))
      } else if (stack.contains(w)) {
        lowl(v) = math.min(lowl(v), index(w))
      }
    }

    if (lowl(v) == index(v)) {
      val scc = Buffer.empty[TP]
       
      var over = false
      while(!over) {
        var p = stack.pop()
        scc += p
        if(v == p)
          over = true
      }
 
        result += scc
    }
  }

  for (v <- g.keys) 
    if (!lowl.contains(v)) 
      visit(v)
     
  result
}

}