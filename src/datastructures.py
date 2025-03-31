
class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self._members = []

    def add_member(self, member):
        if "id" not in member:
            raise ValueError("Agrega ID.")
        member["last_name"] = self.last_name
        member["lucky_numbers"] = list(member.get("lucky_numbers", set()))
        self._members.append(member)

        return member

    def delete_member(self, id):
        for position in range(len(self._members)):
            if self._members[position]["id"] == id:
                self._members.pop(position)
                return None

    def get_member(self, id):
        for member in self._members:
            if member["id"] == int(id):
                return member
            
        return None

    def get_all_members(self):
        return self._members
