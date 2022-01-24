using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Catan
{
    internal class Player
    {

        public Players color { get; set; }

        public Node<Resource> deck { get; set; }

        public Node<Cards> cards { get; set; }

        public int victory_points { get; set; }

        public Player(Players c)
        {

            this.color = c;

            this.victory_points = 0;

            deck = new Node<Resource>(Resource.None);

            cards = new Node<Cards>(Cards.None);

        }

        public override string ToString()
        {
            return this.color.ToString();
        }

        public bool RemoveResourcesIfAvailable(Node<Resource> resources)
        {

            Node<Resource> tmp = CloneDeck();
            Node<Resource> r_orig = resources;
            while (resources != null)
            {

                Node<Resource> tmp2 = tmp;
                int ind = 0;
                bool found_resource = false;
                while (tmp2 != null)
                {

                    if (resources.GetValue() == tmp2.GetValue())
                    {

                        tmp = RemoveCard(tmp, ind);
                        found_resource = true;
                        break;

                    }
                    ind++;
                    tmp2 = tmp2.GetNext();


                }

                if (!found_resource)
                    return false;

                resources = resources.GetNext();

            }

            while(r_orig != null)
            {

                Node<Resource> tmp3 = deck;
                int ind2 = 0;
                while (tmp3 != null)
                {

                    if (tmp3.GetValue() == r_orig.GetValue())
                    {
                        deck = RemoveCard(deck, ind2);
                        break;
                    }
                    tmp3 = tmp3.GetNext();
                    ind2++;
                }

                r_orig = r_orig.GetNext();

            }

            return true;

        }

        private Node<Resource> CloneDeck()
        {

            Node<Resource> tmp = new Node<Resource>(deck.GetValue());
            Node<Resource> tmp_orig = tmp;
            Node<Resource> tmp_deck = deck;
            tmp_deck = tmp_deck.GetNext();

            while (tmp_deck != null)
            {
                tmp.SetNext(new Node<Resource>(tmp_deck.GetValue()));
                tmp_deck = tmp_deck.GetNext();
                tmp = tmp.GetNext();

            }

            return tmp_orig;


        }

        public Node<Resource> RemoveCard(Node<Resource> head, int index)
        {

            int count = 0;

            Node<Resource> pos = head;

            if (index == 0)
                return head.GetNext();

            while (pos.HasNext())
            {

                if (count + 1 == index)
                {

                    pos.SetNext(pos.GetNext().GetNext());
                    return head;

                }

                pos = pos.GetNext();

                count++;

            }

            return head;


        }

        public Resource GetFirst()
        {

            return this.deck.GetValue();

        }

        public static Node<Cards> RemoveDevelopmentCard(Node<Cards> head, int index)
        {

            int count = 0;

            Node<Cards> pos = head;

            if (index == 0)
                return head.GetNext();

            while (pos.HasNext())
            {

                if (count + 1 == index)
                {

                    pos.SetNext(pos.GetNext().GetNext());
                    return head;

                }

                pos = pos.GetNext();

                count++;

            }

            return head;


        }


        internal void GrantResource(Resource resource)
        {

            if (deck.GetValue() == Resource.None)
                deck.SetValue(resource);
            else
                deck = new Node<Resource>(resource, deck);
        }

        internal void GrantCard(Cards c)
        {

            if (cards.GetValue() == Cards.None)
                cards.SetValue(c);
            else
                cards = new Node<Cards>(c, cards);
        }

        public bool UseDevelopmentCard(Cards c)
        {

            if (c == Cards.Vp)
                return false;

            Node<Cards> tmp = cards;

            int ind = 0;
            while (tmp != null)
            {

                if (tmp.GetValue() == c)
                {

                    cards = RemoveDevelopmentCard(cards, ind);
                    return true;

                }
                ind++;
                tmp = tmp.GetNext();

            }

            return false;

        }


    }
}
