import streamlit as st
import simplekml

st.title('緯度経度作成くん')
st.write('google_earthで表示するのに必要なkmlファイルを作成してくれます')
title= st.text_input("NOTAM番号をコピペしてください 👇",)
raw_coordinates = st.text_input("座標をコピペしてください 👇",)
def dms_to_decimal(data):
    data, syousuu = data.split('.')
    seconds = data[-2:] + '.' + syousuu
    minutes = data[-4:-2]
    degrees = data[:-4]
    decimal = int(degrees) + int(minutes) / 60 + float(seconds) / 3600
    return decimal


def coordinate_conversion(input_coordinates):
    result = []

    # 各座標に対して変換
    for input_coordinate in input_coordinates:
        parts = input_coordinate.split('N')
        lat_part = parts[0]  # 緯度
        lon_part = parts[1].replace('E', '')  # 経度

        latitude = round(dms_to_decimal(lat_part), 6)
        longitude = round(dms_to_decimal(lon_part), 6)

        result.append((longitude, latitude))  # タプルの順序を(latitude, longitude)に変更

    return result

if st.button('kmlファイル作成'):
    input_coordinates = [coord for coord in raw_coordinates.replace("\n", " ").split(" ") if coord]

    converted_coordinates = coordinate_conversion(input_coordinates)


    # KMLオブジェクトを作成
    kml = simplekml.Kml()

    # 緯度と経度のリストを作成します
    coords = converted_coordinates

    # 最初の座標をリストの最後に追加して閉じたポリゴンを作成
    coords.append(coords[0])

    # ポリゴン（多角形）を作成
    pol = kml.newpolygon(name="Polygon", outerboundaryis=coords)

    pol.linestyle.color = simplekml.Color.red  # 色の指定
    pol.linestyle.width = 4  # 太さの指定
    pol.polystyle.color = simplekml.Color.changealphaint(0, simplekml.Color.red)  # ポリゴンの塗りつぶしを無効化

    # KMLファイル
    kml.save(f"{title}.kml")

    message=st.empty()
    message.write('作成中です')
    st.success('kmlファイルの出力が完了しました')

    data = open(f"{title}.kml", 'r').read()
    st.download_button(
        label='klmダウンロード',
        data=data,
        file_name=f"{title}.kml"
    )