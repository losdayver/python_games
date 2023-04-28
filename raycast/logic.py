import math
import game

#places angle between 0 and 2pi
def normalize_angle(angle):
    if angle>=2*math.pi:
        angle=angle-2*math.pi
    elif angle<0:
        angle=2*math.pi+angle

    return angle

def angle_exclude_asymptotes(angle):
    if angle in (0, math.pi, math.pi/2, math.pi*3/2):
        angle+=0.0001

    return angle

#returns sign of a number
def sign(value):
    if value>0: return 1
    elif value<0: return -1
    else: return 0



def cast(coords, angle, level, tile, steps):

    symbol = None

    angle = angle_exclude_asymptotes(angle)
    angle = normalize_angle(angle)

    px, py = coords[0], coords[1]
    yclipplane = xclipplane = 0

    if 0 < angle < math.pi:
        yclipplane = (py//tile)*tile
    else:
        yclipplane = (py//tile+1)*tile

    if angle < math.pi/2 or angle > 3/2*math.pi:
        xclipplane = (px//tile+1)*tile
    else:
        xclipplane = (px//tile)*tile

    tg = math.tan(angle)
    #if abs(tg)<0.000001: tg = 0.000001
    atg = 1/tg

    ost=atg*(py-yclipplane)
    ost1=tg*(xclipplane-px)

    xcoll1 = ycoll1 = xcoll2 = ycoll2 = 0
    r = r1 = 100000000
    viewblocked1 = viewblocked2 = False

    for i in range(steps):
        if not viewblocked1:
            xcoll1 = xclipplane+tile*sign(math.cos(angle))*i
            ycoll1 = py-(ost1+sign(math.cos(angle))*tg*tile*i)

        if not viewblocked2:
            xcoll2 = px+(ost+sign(math.sin(angle))*atg*tile*i)
            ycoll2 = yclipplane-tile*sign(math.sin(angle))*i

        sbx = sight_blocked("x", [xcoll1, ycoll1], sign(math.cos(angle)), level, tile)
        sby = sight_blocked("y", [xcoll2, ycoll2], sign(-math.sin(angle)), level, tile)

        if (not viewblocked1) and sbx!='.' and not sbx in game.props:
            r = min([math.dist([px,py],[xcoll1,ycoll1]), r]);
            viewblocked1=True

        if (not viewblocked2) and sby!='.' and not sby in game.props:
            r1 = min([math.dist([px,py],[xcoll2,ycoll2]), r1]);
            viewblocked2=True

        if viewblocked1 and viewblocked2:
            break

    xc = yc = 0

    orient=0

    if r<r1:
        xc, yc = xcoll1, ycoll1
        orient=1
        symbol = sbx
    else:
        xc, yc = xcoll2, ycoll2
        orient=-1
        symbol = sby

    r_final=min(r,r1)

    return [xc, yc, r_final, orient, angle, symbol]

#casts multiple rays, returns list of lists of "cast(...)" information
def cast_multiple(player, level, tile, steps, number_of_rays):
    values = list()

    for i in range(number_of_rays):
        angle1 = player.angle + player.fov*(0.5 - 1/number_of_rays*i)

        cast_info = cast(player.coords, angle1, level, tile, steps)
        cast_info.append(i)
        values.append(cast_info)

    return values

#tests if sight is "blocked"
def sight_blocked(axis, coords, s, lvl, tl):
    x = int(coords[0]//tl)
    y = int(coords[1]//tl)

    if axis == "x":
        x+=sign(s-1)
    elif axis == "y":
        y+=sign(s-1)

    if y<len(lvl) and x<len(lvl[0]) and x>=0 and y>=0 and not lvl[y][x] in game.props:
        return lvl[y][x]

    return '.'

def sight_blocked_prop(axis, coords, s, lvl, tl):
    x = int(coords[0]//tl)
    y = int(coords[1]//tl)

    if axis == "x":
        x+=sign(s-1)
    elif axis == "y":
        y+=sign(s-1)

    if y<len(lvl) and x<len(lvl[0]) and x>=0 and y>=0:
        return (lvl[y][x], (x,y))

    return ('.', None)

def cast_prop(coords, angle, level, tile, steps):
    props=list()

    angle = angle_exclude_asymptotes(angle)
    angle = normalize_angle(angle)

    px, py = coords[0], coords[1]
    yclipplane = xclipplane = 0

    if 0 < angle < math.pi:
        yclipplane = (py//tile)*tile
    else:
        yclipplane = (py//tile+1)*tile

    if angle < math.pi/2 or angle > 3/2*math.pi:
        xclipplane = (px//tile+1)*tile
    else:
        xclipplane = (px//tile)*tile

    tg = math.tan(angle)
    #if abs(tg)<0.000001: tg = 0.000001
    atg = 1/tg

    ost=atg*(py-yclipplane)
    ost1=tg*(xclipplane-px)

    xcoll1 = ycoll1 = xcoll2 = ycoll2 = 0
    viewblocked1 = viewblocked2 = False

    for i in range(steps):
        if not viewblocked1:
            xcoll1 = xclipplane+tile*sign(math.cos(angle))*i
            ycoll1 = py-(ost1+sign(math.cos(angle))*tg*tile*i)

        if not viewblocked2:
            xcoll2 = px+(ost+sign(math.sin(angle))*atg*tile*i)
            ycoll2 = yclipplane-tile*sign(math.sin(angle))*i

        sbx = sight_blocked_prop("x", [xcoll1, ycoll1], sign(math.cos(angle)), level, tile)
        sby = sight_blocked_prop("y", [xcoll2, ycoll2], sign(-math.sin(angle)), level, tile)

        if (not viewblocked1) and sbx[0]!='.' and sbx[0] in game.tiles:
            viewblocked1=True
        elif sbx[0] in game.props:
            try:
                if not (sbx[1][0], sbx[1][1]) in props:
                    props.append((sbx[1][0], sbx[1][1]))
            except: pass

        if (not viewblocked2) and sby[0]!='.' and sby[0] in game.tiles:
            viewblocked2=True
        elif sby[0] in game.props:
            try:
                if not (sby[1][0], sby[1][1]) in props:
                    props.append((sby[1][0], sby[1][1]))
            except: pass

        if viewblocked1 or viewblocked2:
            return props

    return props

def cast_multiple_prop(player, level, tile, steps, number_of_rays):
    props = list()

    for i in range(number_of_rays):
        angle1 = player.angle + player.fov*(0.5 - 1/number_of_rays*i)

        props1 = cast_prop(player.coords, angle1, level, tile, steps)

        for p in props1:
            if not p in props:
                props.append(p)

    return props