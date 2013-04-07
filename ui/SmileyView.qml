import QtQuick 1.0

Rectangle {
    width: 300; height: 200


    GridView {
        id: grid
        anchors.fill: parent
        cellWidth: 30; cellHeight: 30

        model: SmileyModel
        delegate: SmileyDelegate {}
        highlight: Rectangle { color: "lightsteelblue"; radius: 5 }
        focus: true
    }
}
