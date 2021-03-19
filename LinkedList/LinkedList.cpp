//I did it in C++ because it makes more sense
//for this and you can use pointers
#include <iostream>

using namespace std;

template<class T>
struct Node
{
	T data;
	Node<T> *pointer;
	
	Node(T idata, Node<T> *ipointer=NULL)
	{
		data = idata;
		pointer = ipointer;
	}
};

template<class T>
class LinkedList
{
private:
	Node<T> *head;
	Node<T> *tail;
	
public:
	LinkedList<T>()
	{
		head = NULL;
		tail = NULL;
	}
	
	void Traverse()
	{ //Prints every item in order to the console.
		Node<T> *cur = head;
		while (cur != NULL)
		{
			cout << cur->data << " ";
			cur = cur->pointer;
		}
		return;
	}
	
	void Add(T data)
	{ //Adds an item to the end of the list.
		if (head == NULL) {
			head = new Node<T>(data);
			tail = head;
		} else {
			Node<T> *next = new Node<T>(data);
			tail->pointer = next;
			tail = next;
		}
		return;
	}
	
	void Insert(T data, int index)
	{ //Inserts an item at a specified index.
		if (index == 0) {
			head = new Node<T>(data, head);
			return;
		}
		Node<T> *cur = head;
		for (int i = 0; i < index - 1; i++) cur = cur->pointer;
		cur->pointer = new Node<T>(data, cur->pointer);
		if (cur == tail) tail = cur->pointer;
		return;
	}
	
	void Delete(int index)
	{ //Deletes the item at a specified index.
		if (index == 0) {
			head = head->pointer;
			return;
		}
		Node<T> *cur = head;
		for (int i = 0; i < index - 1; i++) cur = cur->pointer;
		cur->pointer = (cur->pointer)->pointer;
		return;
	}

	int Search(T data)
	{ //Searches for an item, and returns the first index at which it appears.
	  //Returns -1 if the item is not found.
		Node<T> *cur = head;
		int i = 0;
		while (cur != NULL)
		{
			if (cur->data == data) return i;
			cur = cur->pointer;
			i++;
		}
		return -1;
	}

    void Dispose()
    { //Disposes of the list.
        Node<T> *prev;
        Node<T> *cur = head;
		while (cur != NULL)
        {
            prev = cur;
            cur = cur->pointer;
            delete prev;
        }
        delete cur;
    }
};


int main()
{ //Tests
	LinkedList<int> a;
	a.Add(5);
	a.Add(7);
	a.Add(24);
	a.Traverse(); //5 7 24
	cout << "\n";
	a.Insert(25, 2);
	a.Delete(0);
	a.Traverse(); //7 25 24
	cout << "\n";
	cout << a.Search(7) << "\n"; //0
	cout << a.Search(17) << "\n"; //-1
    a.Dispose();
	return 0;
}
