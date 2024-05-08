#include <iostream>
#include <vector>
#include <string>
#include <pcl/point_cloud.h>
#include <pcl/point_types.h>
#include <pcl/io/pcd_io.h>
#include <pcl/kdtree/kdtree_flann.h>

// Define classes and structures

class DataPacket {
private:
    pcl::PointCloud<pcl::PointXYZ>::Ptr pointCloud;
public:
    DataPacket() : pointCloud(new pcl::PointCloud<pcl::PointXYZ>) {}
    void addPoint(float x, float y, float z) {
        pcl::PointXYZ point;
        point.x = x;
        point.y = y;
        point.z = z;
        pointCloud->points.push_back(point);
    }
    pcl::PointCloud<pcl::PointXYZ>::Ptr getPointCloud() const { return pointCloud; }
};

class Sender {
public:
    Sender() {}
    void sendData(const DataPacket& packet) {
        std::cout << "Sending point cloud data to point B...\n";
        pcl::io::savePCDFileASCII("point_cloud.pcd", *packet.getPointCloud());
    }
};

class Receiver {
public:
    Receiver() {}
    DataPacket receiveData() {
        std::cout << "Receiving point cloud data from point A...\n";
        DataPacket packet;
        pcl::io::loadPCDFile("point_cloud.pcd", *packet.getPointCloud());
        return packet;
    }
};

// Main function

int main() {
    Sender sender;
    Receiver receiver;

    // Generate point cloud data
    DataPacket pointCloudData;
    pointCloudData.addPoint(1.0, 2.0, 3.0);
    pointCloudData.addPoint(4.0, 5.0, 6.0);
    pointCloudData.addPoint(7.0, 8.0, 9.0);

    // Send point cloud data from point A to point B
    sender.sendData(pointCloudData);

    // Receive point cloud data at point B
    DataPacket receivedData = receiver.receiveData();

    // Perform computations on received point cloud data
    pcl::PointCloud<pcl::PointXYZ>::Ptr receivedPointCloud = receivedData.getPointCloud();
    pcl::KdTreeFLANN<pcl::PointXYZ> kdtree;
    kdtree.setInputCloud(receivedPointCloud);

    // Perform nearest neighbor search
    std::vector<int> pointIdxNKNSearch(3);
    std::vector<float> pointNKNSquaredDistance(3);
    pcl::PointXYZ searchPoint;
    searchPoint.x = 0.0;
    searchPoint.y = 0.0;
    searchPoint.z = 0.0;
    kdtree.nearestKSearch(searchPoint, 3, pointIdxNKNSearch, pointNKNSquaredDistance);
}