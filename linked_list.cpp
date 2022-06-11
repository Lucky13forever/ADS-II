#include <iostream>
using namespace std;
class List{
    private:
        class Node{
            private:
                Node * next;
                Node * prev;
                int val;
            public:
                Node(int);
                const int get_val() const {return val;};
                Node * go_next() {return next;};
                Node * go_prev() {return prev;};
                void set_next(Node * aux) {this->next = aux;};
                void set_prev(Node * aux) {this->prev = aux;};
        };

    Node * first;
    Node * last;
    int size = 0;
    public:
        List();
        void insert(int);
        void afisare();
        void afisare_reverse();
};
List::List()
{
    first = nullptr;
    last = nullptr;
    size = 0;
}
List::Node::Node(int x)
{
    val = x;
    next = nullptr;
    prev = nullptr;
}
void List::insert(int x)
{
    Node * nou = new Node(x);
    if (size == 0)
    {
        first = nou;
        last = nou;
        size = 1;
    }
    else
    {
        last->set_next(nou);
        nou->set_prev(last);
        last = last->go_next();
        size += 1;
    }
}
void List::afisare_reverse()
{
    Node * aux = last;
    for(int i=1; i<=size; i++)
    {
        cout<<aux->get_val()<<" ";
        aux = aux->go_prev(); 
    }
}
void List::afisare()
{
    Node * aux = first;
    for(int i=1; i<=size; i++)
    {
        cout<<aux->get_val()<<" ";
        aux = aux->go_next();
    }
}
int main()
{
    List l;
    l.insert(5);
    l.insert(3);
    l.insert(2);
    l.insert(10);
    l.insert(15);
    l.afisare();
    cout<<"\n";
    l.afisare_reverse();
    return 0;
}
