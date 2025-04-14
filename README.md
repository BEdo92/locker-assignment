#Locker Assignment Tool (API)#
##Overview##
I enjoy swimming, but I've noticed that many swimming pools assign lockers in a way that places guests close to each other, even when the changing room is mostly empty. This can be inconvenient when getting dressed. To address this, I've developed a custom locker assignment logic.

##How It Works##
Locker Sections: The changing room is divided into rows of lockers.

##Assignment Logic:##
- Initially, lockers are assigned starting from the first row, then the second, and so on.
- After filling the rows, the system assigns lockers from the middle of each row, alternating between rows.
- Group Assignments: When multiple guests arrive together (e.g., a family or friends), the system attempts to assign lockers next to each other.

##Current Status##
Interface: The application is built as a Command-Line Interface (CLI).

F##unctionality:##
- The system receives the number of new guests and assigns lockers accordingly.
- It also handles guest departures by freeing up lockers when guests return their "armbands" (which contain locker information).

##Future Plans:##
- Additional testing is needed.
- File handling will be incorporated.
