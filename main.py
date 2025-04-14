from collections import namedtuple
import random

LockerSection = namedtuple('LockerSection', ['section', 'start', 'end'])
UsedSection = namedtuple('UsedSection', ['locker', 'section'])

locker_sections = [
    LockerSection('a0', 1, 10),
    LockerSection('b0', 31, 40),
    LockerSection('c0', 61, 70),
    LockerSection('a1', 11, 20),
    LockerSection('b1', 41, 50),
    LockerSection('c1', 71, 80),
    LockerSection('a2', 21, 30),
    LockerSection('b2', 51, 60),
    LockerSection('c2', 81, 90),
]

sections_to_use = list(reversed(locker_sections)) 
used_lockers = []

def add_locker(num):
    try_counter = 0
    if len(sections_to_use) == 0:
        sections_to_use.clear()
        sections_to_use.extend(reversed(locker_sections)) 
    while try_counter <= len(sections_to_use):
        section = sections_to_use.pop()
        print(f"current section is: {section.section}")
        try_counter += 1

        used_in_section = sum(1 for u in used_lockers if u.section == section.section)
        available_in_section = section.end - section.start + 1 - used_in_section
        print(f"number of available lockers: {available_in_section}")

        if available_in_section == num:
            available_lockers = [i for i in range(section.start, section.end + 1)
                                 if UsedSection(i, section.section) not in used_lockers]
            used_lockers.extend([UsedSection(i, section.section) for i in available_lockers[:num]])
            used_lockers.sort(key=lambda x: x.section)
            break
        elif available_in_section > num:
            section_used = sorted([u.locker for u in used_lockers if u.section == section.section])
            biggest_start = section.start - 1
            biggest_size = 0

            if not section_used:
                # all lockers are free
                range_size = section.end - section.start + 1 - num
                if range_size < 0:
                    continue 
                start_idx = section.start + random.randint(0, range_size)
                for i in range(start_idx, start_idx + num):
                    used_lockers.append(UsedSection(i, section.section))
                break

            # searching for the biggest gap between used lockers
            # include the start and end of the section in the list of used lockers
            section_used.append(section.start)
            section_used.append(section.end)
            section_used.sort()
            for i in range(len(section_used) - 1):
                gap = section_used[i + 1] - section_used[i] - 1 
                if gap > biggest_size:
                    biggest_size = gap
                    biggest_start = section_used[i]
                    
            # if the biggest gap is big enough, it assignes lockers in the middle of the gap
            if biggest_size > num:
                #start_idx = ((biggest_start + biggest_size + biggest_start) // 2) - num // 2
                start_idx = (biggest_start + biggest_size // 2) - num // 2
                for i in range(start_idx, start_idx + num):
                    used_lockers.append(UsedSection(i, section.section))
            # if the biggest gap is not big enough, it assigns lockers to the remaining places
            else:
                available_lockers = [i for i in range(section.start, section.end + 1)
                                    if UsedSection(i, section.section) not in used_lockers]
                used_lockers.extend([UsedSection(i, section.section) for i in available_lockers[:num]])
                used_lockers.sort(key=lambda x: x.section)
            break
        sections_to_use.append(section)
    print_lockers()

def free_locker(locker_num):
    to_remove = [u for u in used_lockers if u.locker == locker_num]
    for u in to_remove:
        used_lockers.remove(u)
        for section in locker_sections:
            if u.section == section.section and section not in sections_to_use:
                sections_to_use.append(section)
                break
    print_lockers()    

def print_lockers():
    all_sections_sorted = sorted(locker_sections, key=lambda s: s.start)
    used_locker_nums = [s.locker for s in used_lockers]
    for i in range(len(all_sections_sorted)):
        if i > 0 and all_sections_sorted[i].section[0] != all_sections_sorted[i - 1].section[0]:
            print()
        for locker in range(all_sections_sorted[i].start, all_sections_sorted[i].end + 1):
            if locker in used_locker_nums:
                print(str(locker).center(4, '|'), end=' ')
            else:
                print(str(locker).center(4, '-'), end=' ')
    print()

if __name__ == '__main__':
    total_guests = 0
    current_guests = 0
    print('Welcome!')
    print('Desired input format is:')
    print('n 1 - for 1 new guest; increase the number accordingly')
    print('e 13 - when guest exits, with the number of their locker')
    print('q - for quit the program')
    
    while True:
        cmd = input().split()
        if len(cmd) > 1 and cmd[0] == 'n':
            if int(cmd[1]) > 10:
                print('maximum number of 10 lockers can be reserved within a section')
                continue
            total_guests += int(cmd[1])
            current_guests += int(cmd[1])
            add_locker(int(cmd[1]))
            print(f"new guest(s) arrived - {cmd[1]} current guests - {current_guests}")
            print(f"total guests - {total_guests}")
        elif len(cmd) > 1 and cmd[0] == 'e':
            if current_guests == 0:
                print('Invalid command - already no guests')
                continue
            print(f"guest left - locker: {cmd[1]}")
            print(f"total guests - {total_guests}")
            free_locker(int(cmd[1]))
            current_guests -= 1
            print(f"total guests - {total_guests}; current guests - {current_guests}")
        elif cmd[0] == 'q':
            print('Are you really want to quit? y/n')
            if input() == 'y':
                break
        else:
            print('Invalid command')

        if current_guests > 90:
            print('Maximum number of lockers is 90 - all lockers are reserved')
