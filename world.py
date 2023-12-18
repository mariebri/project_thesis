import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy.spatial import ConvexHull

class World:
    def __init__(self):
        # Ports
        self.portA = np.array([570506, 7035798, np.deg2rad(30)])
        self.portB = np.array([570366, 7035194, np.deg2rad(20)])
        self.portC = np.array([569877, 7034895, np.deg2rad(80)])
        self.portD = np.array([569475, 7034730, np.deg2rad(80)])
        self.portE = np.array([570016, 7034409, np.deg2rad(140)])

        # Operating Area
        self.nSets = 0
        self.convexSets = []
        self.convexIneqs = []
        self.setNames = []
        self.hasPort = []
        self.connectionPoints = []
        self.connectionIndices = []
        self.ports = {}

        # Initializing environment
        self.initializeWorld()

    def initializeWorld(self):
        self.addSet(np.array([[905,0], [724,431], [788,448], [1008,0]]), 'A-Transit', False)
        self.addSet(np.array([[893,15], [920,22], [910,58], [880,50]]), 'A', True, self.portA)
        self.addSet(np.array([[724,388], [805,407], [677,642], [652,618]]), 'B-Transit', False)
        self.addSet(np.array([[779,451], [756,445], [747,463], [768,470]]), 'B', True, self.portB)
        self.addSet(np.array([[661,594], [696,609], [608, 797], [583, 790]]), 'B-Cross', False)
        self.addSet(np.array([[569,737], [559,763], [610,788], [632,745]]), 'Cross', False)
        self.addSet(np.array([[524,718], [519,739], [583,775], [569,739]]), 'Cross-C1', False)
        self.addSet(np.array([[460,688], [455,710], [527,740], [534,728]]), 'Cross-C2', False)
        self.addSet(np.array([[327,676], [327,699], [465,710], [467,688]]), 'C-Transit', False)
        self.addSet(np.array([[344,677], [344,690], [360,692], [361,680]]), 'C', True, self.portC)
        self.addSet(np.array([[344,676], [343,701], [144,711], [144,692]]), 'D-Cross', False)
        self.addSet(np.array([[154,688], [159,711], [26,788], [13,756]]), 'D-Transit', False)
        self.addSet(np.array([[29,783], [22,765], [43,759], [48,773]]), 'D', True, self.portD)
        self.addSet(np.array([[616,772], [594,761], [455, 1044], [499, 1044]]), 'E-Transit', False)
        self.addSet(np.array([[473,1007], [486,1014], [479,1035], [461,1030]]), 'E', True, self.portE)

        self.addSet(np.array([[893,15], [920,22], [910,58], [880,50]]), 'A-port', False)
        self.addSet(np.array([[779,451], [756,445], [747,463], [768,470]]), 'B-port', False)
        self.addSet(np.array([[344,677], [344,690], [360,692], [361,680]]), 'C-port', False)
        self.addSet(np.array([[29,783], [22,765], [43,759], [48,773]]), 'D-port', False)
        self.addSet(np.array([[473,1007], [486,1014], [479,1035], [461,1030]]), 'E-port', False)
        self.addConnection('A', 'A-port', self.portA[:2], self.portA[2], np.deg2rad(30))
        self.addConnection('B', 'B-port', self.portB[:2], self.portB[2], np.deg2rad(-140))
        self.addConnection('C', 'C-port', self.portC[:2], self.portC[2], np.deg2rad(90))
        self.addConnection('D', 'D-port', self.portD[:2], self.portD[2], np.deg2rad(-60))
        self.addConnection('E', 'E-port', self.portE[:2], self.portE[2], np.deg2rad(-70))

        self.addConnection('A', 'A-Transit', np.array([570519, 7035785]), np.deg2rad(70), np.deg2rad(-120))
        self.addConnection('B', 'B-Transit', np.array([570349, 7035203]), np.deg2rad(160), np.deg2rad(20))
        self.addConnection('C', 'C-Transit', np.array([569878, 7034874]), np.deg2rad(90), np.deg2rad(-90))
        self.addConnection('D', 'D-Transit', np.array([569480, 7034746]), np.deg2rad(-60), np.deg2rad(60))
        self.addConnection('E', 'E-Transit', np.array([570032, 7034419]), np.deg2rad(-60), np.deg2rad(120))
        self.addConnection('A-Transit', 'B-Transit',np.array([570375, 7035276]), np.deg2rad(110), np.deg2rad(-80))
        self.addConnection('B-Transit', 'B-Cross',  np.array([570196, 7034853]), np.deg2rad(120), np.deg2rad(-60))
        self.addConnection('Cross', 'B-Cross',      np.array([570162, 7034777]), np.deg2rad(-60), np.deg2rad(0))
        self.addConnection('B-Cross', 'E-Transit',  np.array([570173, 7034740]), np.deg2rad(100), np.deg2rad(-60))
        self.addConnection('Cross', 'Cross-C1',     np.array([570116, 7034792]), np.deg2rad(170), np.deg2rad(-10))
        self.addConnection('Cross', 'E-Transit',    np.array([570173, 7034740]), np.deg2rad(120), np.deg2rad(-60))
        self.addConnection('Cross-C1', 'Cross-C2',  np.array([569932, 7034863]), np.deg2rad(-140), np.deg2rad(40))
        self.addConnection('Cross-C2', 'C-Transit', np.array([570012, 7034856]), np.deg2rad(-160), np.deg2rad(20))
        self.addConnection('C-Transit', 'D-Cross',  np.array([569744, 7034876]), np.deg2rad(170), np.deg2rad(-10))
        self.addConnection('D-Cross', 'D-Transit',  np.array([569617, 7034845]), np.deg2rad(150), np.deg2rad(-10))

    def plotMap(self):
        img = np.asarray(Image.open('./Map/Map_flight_wo_name.png'))
        plt.imshow(img, extent=[569463, 570692, 7034366, 7035859])
        plt.text(self.portA[0], self.portA[1], "A", color="white", verticalalignment="bottom")
        plt.text(self.portB[0], self.portB[1], "B", color="white", verticalalignment="top")
        plt.text(self.portC[0], self.portC[1], "C", color="white", verticalalignment="bottom")
        plt.text(self.portD[0], self.portD[1], "D", color="white", horizontalalignment="right")
        plt.text(self.portE[0], self.portE[1], "E", color="white", horizontalalignment="right")

    def convexsetGenerator(self, p):
        A = []
        b = []
        conv_set = []
        added_idx = []
        hull = ConvexHull(p)
        n_points = len(hull.vertices)

        for k in range(n_points):
            i, j = hull.vertices[k-1], hull.vertices[k]
            dx_k = p[j][0] - p[i][0]
            dy_k = p[j][1] - p[i][1]
            if dx_k == 0:
                A_k = [1, 0]
                b_k = p[j][0]
            elif dy_k == 0:
                A_k = [0, 1]
                b_k = p[j][1]
            else:
                a_k = dy_k/dx_k
                A_k = [-a_k, 1]
                b_k = p[j][1] - a_k*p[j][0]

            idx = i
            for _ in range(n_points):
                idx += 1
                if (idx % n_points) != j:
                    idx = idx % n_points
                    break
            
            if np.array(A_k) @ np.array(p[idx]) > b_k:
                A_k[0] *= -1
                A_k[1] *= -1
                b_k *= -1

            if i not in added_idx:
                conv_set.append(p[i])
                added_idx.append(i)

            A.append(A_k)
            b.append(b_k)

        conv_set = np.array(conv_set)
        conv_set.sort(axis=0)
        return np.array(A), np.array(b), hull.vertices
    
    def addSet(self, convexSet, name, hasPort, port=[]):
        self.nSets += 1
        self.convexSets.append(convexSet)
        A, b, _ = self.convexsetGenerator(convexSet.tolist())
        self.convexIneqs.append({'A': A, 'b': b})
        self.setNames.append(name)
        self.hasPort.append(hasPort)
        self.connectionPoints.append([])
        self.connectionIndices.append([])
        if hasPort:
            self.ports[name] = port

    def addConnection(self, name_from, name_to, connection_point, heading_to, heading_from):
        index_from = self.setNames.index(name_from)
        index_to = self.setNames.index(name_to)
        self.connectionIndices[index_from].append(index_to)
        self.connectionIndices[index_to].append(index_from)
        self.connectionPoints[index_from].append(np.concatenate((connection_point, np.array([heading_to]))))
        self.connectionPoints[index_to].append(np.concatenate((connection_point, np.array([heading_from]))))

    def findPath(self, start, goal, counter=0, last_index=-1):
        index_start = self.setNames.index(start)
        for connected_index in self.connectionIndices[index_start]:
            counter += 1
            if counter > 20:
                return []
            
            if last_index == -1 or connected_index != last_index:
                new_start = self.setNames[connected_index]
                if new_start == goal:
                    return [new_start]
                path = self.findPath(new_start, goal, counter, last_index=index_start)
                if path != []:
                    return [new_start] + path
        return []

    def getTransitInfo(self, area_in, area_to):
        index_area_in = self.setNames.index(area_in)
        harbor_ineq = self.convexIneqs[index_area_in]
        index_area_to = self.setNames.index(area_to)
        index_connection = self.connectionIndices[index_area_in].index(index_area_to)
        eta_d = self.connectionPoints[index_area_in][index_connection]

        return eta_d, harbor_ineq

    def checkSwitchedArea(self, area_in, area_to, eta):
        index_area_in = self.setNames.index(area_in)
        index_area_to = self.setNames.index(area_to)
        if index_area_to not in self.connectionIndices[index_area_in]:
            return False, area_in
        index_connection = self.connectionIndices[index_area_in].index(index_area_to)
        eta_d = self.connectionPoints[index_area_in][index_connection]
        if np.linalg.norm(eta[:2] - eta_d[:2]) < 9:
            return True, area_to
        return False, area_in

    def getPort(self, area):
        index_area = self.setNames.index(area)
        if not self.hasPort[index_area]:
            return ''
        return self.ports[area]

    def getAreaIneqs(self, area):
        index_area = self.setNames.index(area)
        return self.convexIneqs[index_area]

    def plot(self, showConvex=False, showInd=False):
        self.plotMap()
        if showConvex:      
            for convex_set in self.convexSets:
                convex_set_wrapped = np.concatenate((convex_set, convex_set[0,:][np.newaxis,:]), axis=0)
                plt.plot(convex_set_wrapped[:,0], convex_set_wrapped[:,1], color='red')

            for connection_point in self.connectionPoints:
                if len(connection_point) > 0:
                    for p in connection_point:
                        plt.plot(p[0], p[1], 'r+')

        if showInd and not showConvex:
            for connection_point in self.connectionPoints:
                if len(connection_point) > 0:
                    for p in connection_point:
                        plt.plot(p[0], p[1], 'r+')
        else:
            return

    def plotLocalArea(self, area_name):
        self.plotMap()
        index_area = self.setNames.index(area_name)
        convex_set_area = self.convexSets[index_area]
        convex_set_wrapped = np.concatenate((convex_set_area, convex_set_area[0,:][np.newaxis,:]), axis=0)
        plt.plot(convex_set_wrapped[:,0], convex_set_wrapped[:,1], color='red')
        xmax = np.max(convex_set_area[:,1]) + 10
        xmin = np.min(convex_set_area[:,1]) - 10
        ymax = np.max(convex_set_area[:,0]) + 10
        ymin = np.min(convex_set_area[:,0]) - 10

        plt.xlim([xmin, xmax])
        plt.ylim([ymin, ymax])