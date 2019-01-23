from app import db
from app.models import Group, SubGroup, SubSubGroup
from app.models import Food, Component, FoodComponent
from app.models import Source, User

import xml.etree.ElementTree
import os


def register(app):
    @app.cli.group()
    def initdb():
        app.logger.info('Init DB')


    @initdb.command()
    def admin():
        email = input('Please enter the admin email: ')
        password = input('Please enter the admin password: ')
        admin = User(username='admin', email=email)
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()


    def import_groups():
        app.logger.info('Importing groups...')
        e = xml.etree.ElementTree.parse('data/alim_grp_2017-11-21.xml').getroot()
        prev_group = None
        prev_sgroup = None
        prev_ssgroup = None
        for alim_grp in e.findall('ALIM_GRP'):
            group = Group(id=int(alim_grp[0].text), name_fr=alim_grp[1].text, name_en=alim_grp[2].text)
            sgroup = SubGroup(id=int(alim_grp[3].text), name_fr=alim_grp[4].text, name_en=alim_grp[5].text)
            ssgroup = SubSubGroup(code=int(alim_grp[6].text), name_fr=alim_grp[7].text, name_en=alim_grp[8].text)

            if group != prev_group:
                prev_group = group
                db.session.add(prev_group)
                db.session.commit()
            if sgroup != prev_sgroup:
                prev_sgroup = sgroup
                db.session.add(prev_sgroup)
                db.session.commit()
            if ssgroup != prev_ssgroup:
                prev_ssgroup = ssgroup
                db.session.add(prev_ssgroup)
                db.session.commit()

    def import_foods():
        app.logger.info('Importing foods...')
        e = xml.etree.ElementTree.parse('data/alim_2017-11-21.xml').getroot()
        for e_food in e.findall('ALIM'):
            food = Food(
                id=int(e_food[0].text),
                name_fr=e_food[1].text,
                name_en=e_food[3].text,
                sub_sub_group_id=int(e_food[7].text)
            )
            db.session.add(food)
        db.session.commit()


    def import_components():
        app.logger.info('Importing components...')
        e = xml.etree.ElementTree.parse('data/const_2017-11-21.xml').getroot()
        for e_component in e.findall('CONST'):
            component = Component(
                id=int(e_component[0].text),
                name_fr=e_component[1].text,
                name_en=e_component[2].text,
            )
            db.session.add(component)
        db.session.commit()


    def import_sources():
        app.logger.info('Importing sources...')
        e = xml.etree.ElementTree.parse('data/sources_2017-11-21.xml').getroot()
        for e_source in e.findall('SOURCES'):
            source = Source(
                code=int(e_source[0].text),
                ref_citation=e_source[1].text
            )
            db.session.add(source)
        db.session.commit()


    def import_food_component():
        app.logger.info('Importing food components...')
        root = xml.etree.ElementTree.parse('data/compo_2017-11-21.xml').getroot()
        for e in root.findall('COMPO'):
            food_component = FoodComponent(
                quantity = e[2].text,
                min = float(e[3].text.replace(',', '.')) if e[3].text else None,
                max = float(e[4].text.replace(',', '.')) if e[4].text else None,
                trust_code = e[5].text if e[5].text else None,

                food_id = int(e[0].text),
                component_id = int(e[1].text),
                source_id = int(e[6].text) if e[6].text else None
            )
            db.session.add(food_component)
        db.session.commit()


    @initdb.command()
    def importxml():
        import_groups()
        import_foods()
        import_components()
        import_sources()
        import_food_component()


    def empty_table(Table):
        app.logger.info('Deleting the table "{}" content'.format(Table.__name__))
        for row in Table.query.all():
            db.session.delete(row)
        db.session.commit()


    @initdb.command()
    def resetfood():
        empty_table(Group)
        empty_table(SubGroup)
        empty_table(SubSubGroup)
        empty_table(Food)
        empty_table(Component)
        empty_table(Source)
        empty_table(FoodComponent)
