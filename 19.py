class Worker:
    def __init__(self, path):
        self.scanners = []
        scanner = None
        beacons = []
        self.linked = []
        with open(path, 'r') as f:
            for line in f.readlines():
                line = line.replace('\n', '')
                if not line:
                    continue
                if 'scanner' in line:
                    if scanner:
                        scanner.beacons = beacons
                        self.scanners.append(scanner) 
                    number = int(line.split('--- scanner ')[1].split(' ')[0])
                    scanner = Scanner(number)
                    beacons = []
                else:
                    beacons.append(tuple(int(c) for c in line.split(',')))
            scanner.beacons = beacons
            self.scanners.append(scanner) 
        self.link_scanners()
        
    # 19.1    
    def get_number_of_beacons(self):
        s0, *others = self.scanners
        all_beacons = s0.beacons
        for scanner in others:
            all_beacons.extend(scanner.get_beacons_from_scanner_0())
        return len(set(all_beacons))
        
    # 19.2
    def get_max_distance(self):
        s0, *others = self.scanners
        s0.pos_from_0 = (0, 0, 0)
        for scanner in others:
            scanner.pos_from_0 = scanner.get_beacons_from_scanner_0([(0, 0, 0)])[0]
        
        max_dist = 0
        for scanner_1 in self.scanners:
            for scanner_2 in self.scanners:
                if scanner_1.number == scanner_2.number:
                    continue
                dist = scanner_1.get_distance(scanner_2)
                if dist > max_dist:
                    max_dist = dist
        return max_dist
        
    def link_scanners(self, to_link=None):
        to_link = to_link or [self.scanners[0]]
        while to_link:      
            scanner_1 = to_link.pop(0)
            for number_2, scanner_2 in enumerate(self.scanners):
                if scanner_1.number == number_2 or number_2 == 0 or number_2 in self.linked or scanner_2.from_scanner is not None:
                    continue
                result = self.get_diffs(scanner_1.beacons, scanner_2.beacons)
                if result:
                    coords, orientation, mod_x, mod_y, mod_z = result
                    scanner_2.from_scanner = scanner_1
                    scanner_2.coords = coords
                    scanner_2.orientation = orientation
                    scanner_2.mod_x = mod_x
                    scanner_2.mod_y = mod_y
                    scanner_2.mod_z = mod_z
                    to_link.append(scanner_2)
            self.linked.append(scanner_1.number)
                                    
    def get_diffs(self, scans1, scans2):
        for i in range(6):
            for x2 in (-1, 1):
                for y2 in (-1, 1):
                    for z2 in (-1, 1):
                        diffs = {}
                        for p1 in scans1:
                            for p2 in scans2:
                                d = self.diff(p1, p2, x2, y2, z2, i)
                                diffs[d] = (diffs.get(d) or []) + [[p1, p2]]
                            result_12 = [k for k, v in diffs.items() if len(v) >= 12]
                            if result_12:
                                return result_12[0], i, x2, y2, z2                          

    def diff(self, p1, p2, mod_x2, mod_y2, mod_z2, orientation):
        x1, y1, z1 = p1
        if orientation == 0:
            x2, y2, z2 = p2
        elif orientation == 1:
            y2, z2, x2 = p2
        elif orientation == 2:
            z2, x2, y2 = p2
        elif orientation == 3:
            x2, z2, y2 = p2
        elif orientation == 4:
            y2, x2, z2 = p2
        elif orientation == 5:
            z2, y2, x2 = p2
        return (x1 - x2 * mod_x2, y1 - y2 * mod_y2, z1 - z2 * mod_z2)
                

class Scanner:
    def __init__(self, number):
        self.from_scanner = None
        self.number = number
        
    def get_beacons_from_scanner_0(self, beacons=None):
        beacons = beacons or self.beacons
        result = []
        difx, dify, difz = self.coords
        for beacon in beacons:
            if self.orientation == 0:
                bx, by, bz = beacon
            elif self.orientation == 1:
                by, bz, bx = beacon
            elif self.orientation == 2:
                bz, bx, by = beacon
            elif self.orientation == 3:
                bx, bz, by = beacon
            elif self.orientation == 4:
                by, bx, bz = beacon
            elif self.orientation == 5:
                bz, by, bx = beacon
            result.append((difx + self.mod_x * bx, dify + self.mod_y * by, difz + self.mod_z * bz))
        if self.from_scanner.number == 0:
            return result
        else:
            return self.from_scanner.get_beacons_from_scanner_0(beacons=result)
            
    def get_distance(self, other_scanner):
        x1, y1, z1 = self.pos_from_0
        x2, y2, z2 = other_scanner.pos_from_0
        return sum([abs(x1 - x2), abs(y1 - y2), abs(z1 - z2)])
