using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Queue
{
    class Node<T>
    {
        private T value;
        private Node<T> next;

        public Node(T value, Node<T> next)
        {
            this.value = value;
            this.next = next;
        }
        public Node(T value)
        {
            this.value = value;
            this.next = null;
        }

        public void SetValue(T value)
        {
            this.value = value;
        }
        public void SetNext(Node<T> next)
        {
            this.next = next;
        }
        public T GetValue()
        {
            return this.value;
        }
        public Node<T> GetNext()
        {
            return this.next;
        }
        public override string ToString()
        {
            return this.value.ToString();
        }
        public bool HasNext()
        {
            return next != null;
        }
    }
}
