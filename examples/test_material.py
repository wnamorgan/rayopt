
import rayopt as ro

def main():
    material = "N-BK7"
    material = "N-SK4"
    material = "F4"
    material = "B270"
    get_material_info(material)

def get_material_info(material):
    lib = ro.Library.one()
    for g in lib.session.query(
        ro.library.Material).filter(
        ro.library.Material.name.contains(material)):
        print(g.name, g.catalog.name, g.catalog.source)

if __name__=='__main__':
    main()