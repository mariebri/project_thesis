import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy.spatial import ConvexHull

class World:
    def __init__(self):
        # Ports
        x0, y0 = 569463, 7034366
        x_mult = (570692-569463)/1045
        y_mult = (7035859-7034366)/1045
        self.portA = np.array([888*x_mult + x0, 35*y_mult + y0, np.deg2rad(30)])
        self.portB = np.array([767*x_mult + x0, 466*y_mult + y0, np.deg2rad(20)])
        self.portC = np.array([353*x_mult + x0, 679*y_mult + y0, np.deg2rad(80)])
        self.portD = np.array([39*x_mult + x0, 780*y_mult + y0, np.deg2rad(80)])
        self.portE = np.array([470*x_mult + x0, 1020*y_mult + y0, np.deg2rad(140)])

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
        x0, y0 = 569463, 7034366
        x_mult = (570692-569463)/1045
        y_mult = (7035859-7034366)/1045

        self.addSet(np.array([[905*x_mult + x0, 0*y_mult + y0], [724*x_mult + x0, 431*y_mult + y0], [788*x_mult + x0, 448*y_mult + y0], [1008*x_mult + x0, 0*y_mult + y0]]), 'A-Transit', False)
        self.addSet(np.array([[893*x_mult + x0,15*y_mult + y0], [920*x_mult + x0,22*y_mult + y0], [910*x_mult + x0,58*y_mult + y0], [880*x_mult + x0,50*y_mult + y0]]), 'A', True, self.portA)
        self.addSet(np.array([[724*x_mult + x0,388*y_mult + y0], [805*x_mult + x0,407*y_mult + y0], [677*x_mult + x0,642*y_mult + y0], [652*x_mult + x0,618*y_mult + y0]]), 'B-Transit', False)
        self.addSet(np.array([[779*x_mult + x0,451*y_mult + y0], [756*x_mult + x0,445*y_mult + y0], [747*x_mult + x0,463*y_mult + y0], [768*x_mult + x0,470*y_mult + y0]]), 'B', True, self.portB)
        self.addSet(np.array([[661*x_mult + x0,594*y_mult + y0], [696*x_mult + x0,609*y_mult + y0], [608*x_mult + x0, 797*y_mult + y0], [583*x_mult + x0, 790*y_mult + y0]]), 'B-Cross', False)
        self.addSet(np.array([[569*x_mult + x0,737*y_mult + y0], [559*x_mult + x0,763*y_mult + y0], [610*x_mult + x0,788*y_mult + y0], [632*x_mult + x0,745*y_mult + y0]]), 'Cross', False)
        self.addSet(np.array([[524*x_mult + x0,718*y_mult + y0], [519*x_mult + x0,739*y_mult + y0], [583*x_mult + x0,775*y_mult + y0], [569*x_mult + x0,739*y_mult + y0]]), 'Cross-C1', False)
        self.addSet(np.array([[460*x_mult + x0,688*y_mult + y0], [455*x_mult + x0,710*y_mult + y0], [527*x_mult + x0,740*y_mult + y0], [534*x_mult + x0,728*y_mult + y0]]), 'Cross-C2', False)
        self.addSet(np.array([[327*x_mult + x0,676*y_mult + y0], [327*x_mult + x0,699*y_mult + y0], [465*x_mult + x0,710*y_mult + y0], [467*x_mult + x0,688*y_mult + y0]]), 'C-Transit', False)
        self.addSet(np.array([[344*x_mult + x0,677*y_mult + y0], [344*x_mult + x0,690*y_mult + y0], [360*x_mult + x0,692*y_mult + y0], [361*x_mult + x0,680*y_mult + y0]]), 'C', True, self.portC)
        self.addSet(np.array([[344*x_mult + x0,676*y_mult + y0], [343*x_mult + x0,701*y_mult + y0], [144*x_mult + x0,711*y_mult + y0], [144*x_mult + x0,692*y_mult + y0]]), 'D-Cross', False)
        self.addSet(np.array([[154*x_mult + x0,688*y_mult + y0], [159*x_mult + x0,711*y_mult + y0], [26*x_mult + x0,788*y_mult + y0], [13*x_mult + x0,756*y_mult + y0]]), 'D-Transit', False)
        self.addSet(np.array([[29*x_mult + x0,783*y_mult + y0], [22*x_mult + x0,765*y_mult + y0], [43*x_mult + x0,759*y_mult + y0], [48*x_mult + x0,773*y_mult + y0]]), 'D', True, self.portD)
        self.addSet(np.array([[616*x_mult + x0,772*y_mult + y0], [594*x_mult + x0,761*y_mult + y0], [455*x_mult + x0, 1044*y_mult + y0], [499*x_mult + x0, 1044*y_mult + y0]]), 'E-Transit', False)
        self.addSet(np.array([[473*x_mult + x0,1007*y_mult + y0], [486*x_mult + x0,1014*y_mult + y0], [479*x_mult + x0,1035*y_mult + y0], [461*x_mult + x0,1030*y_mult + y0]]), 'E', True, self.portE)

        self.addSet(np.array([[893*x_mult + x0,15*y_mult + y0], [920*x_mult + x0,22*y_mult + y0], [910*x_mult + x0,58*y_mult + y0], [880*x_mult + x0,50*y_mult + y0]]), 'A-port', False)
        self.addSet(np.array([[779*x_mult + x0,451*y_mult + y0], [756*x_mult + x0,445*y_mult + y0], [747*x_mult + x0,463*y_mult + y0], [768*x_mult + x0,470*y_mult + y0]]), 'B-port', False)
        self.addSet(np.array([[344*x_mult + x0,677*y_mult + y0], [344*x_mult + x0,690*y_mult + y0], [360*x_mult + x0,692*y_mult + y0], [361*x_mult + x0,680*y_mult + y0]]), 'C-port', False)
        self.addSet(np.array([[29*x_mult + x0,783*y_mult + y0], [22*x_mult + x0,765*y_mult + y0], [43*x_mult + x0,759*y_mult + y0], [48*x_mult + x0,773*y_mult + y0]]), 'D-port', False)
        self.addSet(np.array([[473*x_mult + x0,1007*y_mult + y0], [486*x_mult + x0,1014*y_mult + y0], [479*x_mult + x0,1035*y_mult + y0], [461*x_mult + x0,1030*y_mult + y0]]), 'E-port', False)
        self.addConnection('A', 'A-port', self.portA[:2], self.portA[2], np.deg2rad(30))
        self.addConnection('B', 'B-port', self.portB[:2], self.portB[2], np.deg2rad(-140))
        self.addConnection('C', 'C-port', self.portC[:2], self.portC[2], np.deg2rad(90))
        self.addConnection('D', 'D-port', self.portD[:2], self.portD[2], np.deg2rad(-60))
        self.addConnection('E', 'E-port', self.portE[:2], self.portE[2], np.deg2rad(-70))

        self.addConnection('A', 'A-Transit', np.array([906*x_mult + x0,43*y_mult + y0]), np.deg2rad(70), np.deg2rad(-120))
        self.addConnection('B', 'B-Transit', np.array([750*x_mult + x0,456*y_mult + y0]), np.deg2rad(160), np.deg2rad(20))
        self.addConnection('C', 'C-Transit', np.array([353*x_mult + x0,690*y_mult + y0]), np.deg2rad(90), np.deg2rad(-90))
        self.addConnection('D', 'D-Transit', np.array([41*x_mult + x0,761*y_mult + y0]), np.deg2rad(-60), np.deg2rad(60))
        self.addConnection('E', 'E-Transit', np.array([485*x_mult + x0,1013*y_mult + y0]), np.deg2rad(-60), np.deg2rad(120))
        self.addConnection('A-Transit', 'B-Transit', np.array([750*x_mult + x0,421*y_mult + y0]), np.deg2rad(110), np.deg2rad(-80))
        self.addConnection('B-Transit', 'B-Cross', np.array([670*x_mult + x0, 615*y_mult + y0]), np.deg2rad(120), np.deg2rad(-60))
        self.addConnection('Cross', 'B-Cross', np.array([605*x_mult + x0,756*y_mult + y0]), np.deg2rad(-60), np.deg2rad(0))
        self.addConnection('B-Cross', 'E-Transit', np.array([598*x_mult + x0, 785*y_mult + y0]), np.deg2rad(100), np.deg2rad(-60))
        self.addConnection('Cross', 'Cross-C1', np.array([567*x_mult + x0,752*y_mult + y0]), np.deg2rad(170), np.deg2rad(-10))
        self.addConnection('Cross', 'E-Transit', np.array([598*x_mult + x0, 785*y_mult + y0]), np.deg2rad(120), np.deg2rad(-60))
        self.addConnection('Cross-C1', 'Cross-C2', np.array([527*x_mult + x0,731*y_mult + y0]), np.deg2rad(-140), np.deg2rad(40))
        self.addConnection('Cross-C2', 'C-Transit', np.array([462*x_mult + x0,701*y_mult + y0]), np.deg2rad(-160), np.deg2rad(20))
        self.addConnection('C-Transit', 'D-Cross', np.array([310*x_mult + x0,687*y_mult + y0]), np.deg2rad(170), np.deg2rad(-10))
        self.addConnection('D-Cross', 'D-Transit', np.array([144*x_mult + x0,704*y_mult + y0]), np.deg2rad(150), np.deg2rad(-10))

    def plotMap(self):
        img = np.asarray(Image.open('./Map/Map_flight_wo_name.png'))
        plt.imshow(img, extent=[569463, 570692, 7035859, 7034366])
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