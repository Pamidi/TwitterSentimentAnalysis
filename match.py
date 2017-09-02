from event_hierarchy import Event, EventHierarchy

class Team:
    def __init__(self, a):
        self.name = a

    """TO-DO
    support addition/retrievel of team specific events from DB here
    """

class Match:
    def __init__(self, a, b):
        self.team1 = a
        self.team2 = b
        self.match_event_tree = None

    """
    TO-DO: have a static method to derive the match object from db
    based on the input parameters

    support to add/retrieve match specific events from DB here
    """

    #create the event hierarchy tree here
    def get_event_hierarchy_tree(self):
        """
        TO-DO : make this API generic enough to derive the
        generic events for a cricket match
        + specific events for team a,b(eg: Virat Kohli/ Sachin retirement etc.)
        from DB.

        The static edges should also be persisted in the database

        Create the static part of the tree and return the root node of
        the tree

        Hardcoding the edges for now..
        """
        #Tree structure
        #1.match
        #2.toss, wicket, boundary, powerplay, drinks, innings_break,
        #3.four, six, ith wicket, ith powerplay
        #4. ith four, ith six
        #create root
        root = Event('MATCH-INDIA-SRILANKA')
        l1_n1 = Event('TOSS', keywords= ['toss'])
        l1_n2 = Event('WICKET')
        l1_n3 = Event('BOUNDARY')
        l1_n4 = Event('POWERPLAY')
        l1_n5 = Event('DRINKS', keywords=['drink'])
        l1_n6 = Event('INNINGS_BREAK', keywords=['innings','break'])
        l1_n7 = Event('CENTURY')
        l1_n8 = Event('HALF_CENTURY')
        l1_n9 = Event('HAT-TRICK')
        l1_n10 = Event('MAIDEN')
        l2_n1 = Event('FOUR')
        l2_n2 = Event('SIX')
        l2_n3 = Event('NTH_WICKET', keywords=['wicket','out','lbw','caught','bowled'])
        l2_n4 = Event('ITH_POWERPLAY', keywords=['powerplay'])
        l2_n5 = Event('ITH_CENTURY', keywords=['century','hundred','100'])
        l2_n6 = Event('ITH_HALF_CENTURY',keywords=['fifty','50','half century'])
        l2_n7 = Event('ITH_HAT_TRICK',keywords=['hat-trick'])
        l2_n8 = Event('ITH_MAIDEN',keywords=['maiden'])
        l3_n1 = Event('ITH FOUR', keywords['four'])
        l3_n2 = Event('ITH SIX', keywords=['six'])

        l2_n1.children.append(l3_n1)
        l2_n2.children.append(l3_n2)

        l1_n2.children.append(l2_n3)
        l1_n3.children.append(l2_n1)
        l1_n3.children.append(l2_n2)
        l1_n4.children.append(l2_n4)
        l1_n7.children.append(l2_n5)
        l1_n8.children.append(l2_n6)
        l1_n9.children.append(l2_n7)
        l1_n10.children.append(l2_n8)

        root.children = [l1_n1,l1_n2,l1_n3,l1_n4,l1_n5,l1_n6,l1_n7,l1_n8,l1_n9,l1_n10]

        self.match_event_tree = EventHierarchy(root)
        #aggregate_keyword_for_nodes now
        self.match_event_tree.aggregate_keyword_for_nodes()

        return self.match_event_tree

    def get_match_details(self):
        """
        TO-DO: Model to return this data from DB
        eg: hashtag/user_to_track of match
        """
        return "tweetcricscore"
