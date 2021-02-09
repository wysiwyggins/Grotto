import random

from django.db.models import Count

from mapBuilder.models import Room


class RoomAdjacencyService:
    """Simple random adjacency for connecting rooms

    Usage
    ------

    While generating rooms call ``RoomAdjacencyService().add_room(<room>)``
    passing the newly generated room.

    Alternately, if rooms exist and you want the connections between them
    to be shuffled use ``RoomAdjacencyService().reorgainize_rooms()``

    """
    max_adjacency = 4
    min_adjacency = 1

    def _make_adjacent(self, room, neighbor):
        # check room and neighbor for compliance in max_adjacency
        for _room in (room, neighbor):
            if _room.exits.count() + 1 > self.max_adjacency:
                raise Exception(f"Cannot add more rooms to {_room}")
        room.exits.add(neighbor)

    def _adjacency_candidates(self, room):
        candidates = Room.objects.exclude(id=room.id).annotate(
            num_exits=Count("exits")
        ).filter(num_exits__lt=self.max_adjacency, num_exits__gt=0)
        return list(candidates)

    def reorganize_rooms(self):
        """Will remove all exits from all rooms and generate a new adjacency"""
        rooms = list(Room.objects.all())
        if len(rooms) < 2:
            return
        for room in rooms:
            room.exits.clear()
        starters = random.sample(rooms, k=2)
        self._make_adjacent(starters[0], starters[1])
        for room in rooms:
            if room in starters:
                continue
            self.add_room(room)

    def add_room(self, room):
        """Will find neighbors for a derelict room"""
        # if room already has adjacency then return
        if room.exits.count() > 0:
            return
        # find rooms which can be neighbors
        candidates = self._adjacency_candidates(room=room)

        if candidates:
            desired_adjacency_count = random.randint(
                self.min_adjacency, min(self.max_adjacency, len(candidates)))
            # randomly choose some rooms
            neighbors = random.sample(candidates, k=desired_adjacency_count)
        else:
            # are there no candidates because I'm the only room, or
            #  because the dance card is full?
            if Room.objects.count() > 1:
                # dance card full
                # randomly choose a set of rooms to divorce and squeeze between
                to_split = random.choose(list(Room.objects.exclude(id=room.id)))
                also_to_split = random.choose(list(to_split.exits.all()))
                to_split.exits.remove(also_to_split)
                neighbors = [also_to_split, to_split]
        # make room adjacent to them
        for neighbor in neighbors:
            self._make_adjacent(room, neighbor)
