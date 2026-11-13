# Builds data/gallery.json from data/manifest.json + the curation below.
# Edit the lists here to add, remove, reorder or retitle images, then run:  python tools/build_gallery.py
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
M = {(r['folder'], r['name']): r for r in json.loads((ROOT / 'data/manifest.json').read_text(encoding='utf-8'))}

# page -> folder, then groups of (image name, title)
PAGES = {
 'paintings': ('unsorted', [
  ('Historical', [
   ('dsc00057', 'Chhatrapati Shivaji Maharaj, gilt frame'), ('pan03488', 'Shivaji Maharaj, portrait study'),
   ('img-0572', 'Shivaji Maharaj, detail'), ('dsc00050', 'Shivaji Maharaj, full length'),
   ('pan03428', 'Standing warrior, miniature style'), ('img-0565', 'Shivaji Maharaj with sword'),
   ('img-0556', 'Mavala warrior, miniature style'), ('img-0577', 'Shivaji Maharaj, carved frame'),
   ('pan03584', 'Three panels, ready for delivery'), ('dsc00051', 'Installed in the hall'),
   ('dsc00054', 'A pair, as hung')]),
  ('Portraits', [
   ('img-9549', 'Commissioned portrait, full length'), ('img-9571', 'Commissioned portrait'),
   ('img-9518', 'Seated portrait in oil'), ('img-9530', 'Seated portrait, close'),
   ('asc05355', 'Family patriarch, oil on canvas'), ('img-0061', 'Seated portrait, formal'),
   ('img-20190221-wa0030', 'Young prince, oil'), ('img-20190503-wa0061', 'Royal portrait, seated'),
   ('img-20181217-wa0001', 'Portrait from a photograph'), ('img-20190122-wa0006', 'Portrait in a silk sari'),
   ('img-20220414-wa0008', 'Seated saint, festive colours'), ('img-20200921-wa0001', 'Portrait in saffron'),
   ('16112010301', 'Early portrait, oil'), ('22032012318', 'Portrait, oil on canvas'),
   ('img-20201016-wa0001', 'Portrait, soft ground'), ('img-20191226-wa0001', 'Seated elder'),
   ('makrand-dave', 'Portrait, two studies'), ('img-9561', 'Portrait study')]),
  ('Devotional', [
   ('img-0484', 'Ganesha in the forest'), ('img-0483', 'Meditation'), ('img-0479', 'Into the light'),
   ('img-0480', 'The seeker'), ('img-0482', 'Ascent'), ('img-0481', 'Pilgrim'),
   ('img-20201120-181558', 'Vitthal, temple shrine'), ('img-20201211-wa0090', 'Vitthal, gold ground'),
   ('img-20180529-092426', 'Swami Samarth on the serpent'), ('img-20180529-wa0002', 'Reclining on Shesha'),
   ('img-20200616-130916', 'Swami Samarth'), ('img-20180215-wa0001', 'Durga with lions'),
   ('img-20190731-wa0053', 'Saint in a brick niche'), ('img-20190731-wa0055', 'Sai Baba in a brick niche'),
   ('img-20190731-wa0050', 'Temple doorway'), ('img-20190517-wa0028', 'With Nandi'),
   ('img-9583', 'Trishul'), ('img-9590', 'Khandoba shrine'), ('img-9593', 'Offering'),
   ('modern-2', 'Buddha, palette knife')]),
 ]),
 'paintings-process': ('unsorted', [
  ('Studio', [('img-20201127-174509', 'At the easel'), ('img-9579', 'Detail of the hands'),
              ('img-9577', 'Signed in Marathi'), ('img-0582', 'Framing'), ('img-0583', 'Last checks before delivery'),
              ('dsc00071', 'The finished hall'), ('dsc00073', 'Hung and lit')]),
 ]),
 'sculptures': ('sculptures', [
  ('Busts & figures', [
   ('img-0574', 'Standing figure, bronze finish'), ('img-9316', 'Bust in a pagadi'), ('shivaji-3', 'Shivaji Maharaj, enthroned'),
   ('img-9586', 'Figure with relief backdrop'), ('img-3541', 'Seated Buddha'), ('kasturba-gandhi', 'Kasturba Gandhi'),
   ('img-9319', 'Bust, bronze finish'), ('img-20220621-wa0015', 'Shivaji Maharaj on the throne'),
   ('img-3371', 'Vitthal'), ('img-7516', 'Standing woman, bronze'), ('img-1811', 'Mermaid'),
   ('img-9993', 'Buddha in meditation'), ('img-5020', 'Buddha head, fountain'), ('img-0578', 'Standing figure with garlands'),
   ('phule', 'Mahatma Phule, figure study'), ('shahu', 'Rajarshi Shahu Maharaj, figure study'),
   ('14a40464-d76b-4bf5-af14-002354b4a0e9', 'Kasturba Gandhi, bust'), ('img-7514', 'Award figure on plinth'),
   ('img-9588', 'Relief and figure'), ('img-20220621-wa0017', 'Throne, side view'), ('img-4043', 'Courtyard figure'),
   ('img-5197', 'Head study'), ('baba', 'Standing figure, cut-out')]),
  ('In the workshop', [
   ('7135a56b-1c27-4b6e-af20-9dc54efb6c67', 'Seated figure in clay'), ('img-3297', 'Clay, almost done'),
   ('img-3251', 'Clay, detail'), ('7b8ab856-eb62-4ff7-8e98-dd6d99b9118c', 'Clay, profile'),
   ('img-6278', 'Armature and clay'), ('img-9310', 'Large figure in clay'), ('img-9313', 'Scaffold and figure'),
   ('86247b07-4c81-4b56-b415-6cf425c012ee', 'Vitthal in clay'), ('73e7ec08-1a60-4cdb-8515-fffa76765188', 'Vitthal, finishing'),
   ('img-9329', 'Vitthal, painted'), ('fc49200f-f445-4707-9130-9da9866f2878', 'A procession in fibre'),
   ('ae7094e3-5ddb-45d8-b35e-54cd7619f0a5', 'Life-size figures'), ('img-7561', 'Figure in plaster'),
   ('img-20220621-wa0014', 'Final touches'), ('img-20220621-wa0009', 'Seated figure, unpainted'),
   ('img-20220415-wa0002', 'Tall figure, primed'), ('parsi-1', 'Lamassu'), ('parsi-3', 'Lamassu, front'),
   ('40243129-1843220632452328-3624454572459687936-n', 'Elephants'), ('1055205f-843e-4f24-b984-46a250502065', 'Bullock cart'),
   ('img-3446', 'Garden installation'), ('1ccb324f-5e64-42fd-bcb5-c50712b15978', 'Chariot base')]),
  ('Sets & pandals', [
   ('dsc-9005', 'Temple set, full view'), ('dsc-8995', 'Temple set, stage'), ('dsc-9015', 'Temple set, pillars'),
   ('dsc-9000', 'Temple set, niches'), ('dsc-8996', 'Temple set, gallery'), ('dsc-9012', 'Temple set, centre'),
   ('img-5333', 'Shrine set'), ('img-5337', 'Carved pillar'), ('40100505-1843220532452338-5337868926942445568-n', 'Set under construction'),
   ('img-0002', 'Festival stage'), ('img-0001', 'Festival stage, fireworks'), ('img-0003', 'Festival stage, night'),
   ('img-0004', 'Festival stage, wide'), ('img-0005', 'Festival tower'), ('img-9999', 'On the night'),
   ('rath', 'Rath procession'), ('img-1945', 'Street installation')]),
 ]),
 'murals': ('murals', [
  ('Bhimthadi Jatra gate', [
   ('2', 'Bhimthadi Jatra entrance'), ('img-1611', 'The gate by day'), ('img-1530', 'The gate at dusk'),
   ('img-1602', 'The gate at night'), ('f4e62f4b-03ef-4d65-b5e2-6977af43c6bc', 'Lit for the evening')]),
  ('Swarajya Dhwaj wall', [
   ('img-6530', 'Swarajya Dhwaj wall'), ('j56a8274', 'The full sweep'), ('img-6454', 'Medallions and flag'),
   ('img-6412', 'From the courtyard'), ('img-6520', 'With the team'), ('img-6462', 'The centre panel'),
   ('48e64725-610e-4a78-9f0f-8f9148e8012b', 'Under construction')]),
  ('Relief murals', [
   ('img-0570', 'Relief mural, painted'), ('img-0568', 'Relief mural, in the room'),
   ('a5207181-4812-4bec-a665-cc0a8d2d92e6', 'Instruments wall'), ('img-3395', 'Animal medallions'),
   ('img-3396', 'Medallions, pair'), ('img-3389', 'Tortoise medallion'), ('ebc87309-1d08-4219-a6aa-da3b5474ecbb', 'Shivaji Maharaj, relief'),
   ('180ef56b-e7e0-4054-bcf9-e732d0c18bdf', 'Relief bust in hand'), ('dcd26ca5-2aa3-43da-a307-5052815e2c12', 'Octagonal plaque'),
   ('53180d13-3247-437e-9e2d-d6c247bdc27c', 'Line mural, village'), ('d51d7550-8f2c-4bcd-82e1-e8208ae60527', 'Line mural, with cow'),
   ('img-2804', 'Exhibition wall')]),
 ]),
 'miniature-statues': ('miniature-statues', [
  ('Gifting', [
   ('gb-3801', 'Shivaji Maharaj on horseback'), ('gb-3426', 'Pagadi on a plinth'), ('gb-2309', 'Enthroned, desk piece'),
   ('20230627-215739', 'Buddha head'), ('gb-0677', 'Buddha with carved screen'), ('img-8832', 'Elephant trio'),
   ('gb-3725', 'Horse and rider, silhouette'), ('gb-0838', 'Cannon and seal'), ('gb-3476', 'Pagadi and shankh'),
   ('20230627-215313-01', 'Elephant pair'), ('img-8826', 'Abstract animals'), ('gb-3614', 'Pagadi set'),
   ('dsc-2109', 'India Gate, scale model')]),
 ]),
 'miniature-models': ('models', [
  ('Temple hall model', [
   ('img-5573', 'Through the banyan arch'), ('img-5563', 'The sanctum'), ('img-5560', 'From above'),
   ('img-5565', 'The side gallery'), ('img-5570', 'Niches and murals'), ('img-5571', 'Wall detail'),
   ('img-5574', 'Arch and sanctum'), ('img-5561', 'Front elevation'), ('img-5569', 'Gallery, wide'),
   ('img-5572', 'Banyan roots'), ('img-5567', 'Painted panels'), ('img-5575', 'Plan view')]),
 ]),
}

# Photography: Raigad series, with approximate map positions (lat, lon)
RAIGAD = [
 ('1-alibaug-30-x-20', 'Alibaug Beach', 18.641, 72.872), ('2-kolaba-fort-30-x-20', 'Kolaba Fort', 18.634, 72.864),
 ('3-murud-janjira-30-x-20', 'Murud-Janjira', 18.300, 72.964), ('4-varsoli-30-x-20', 'Varsoli Beach', 18.659, 72.866),
 ('5-kihim-beach-30-x-20-opt-2', 'Kihim Beach', 18.716, 72.861), ('6-akshi-beach-30-x-20', 'Akshi Beach', 18.611, 72.879),
 ('7-karmarkar-30-x-20', 'Karmarkar Sculpture Museum', 18.758, 72.880), ('8-khanderi-underi-30-x-20', 'Khanderi-Underi', 18.705, 72.810),
 ('9-kashid-beach-30-x-20', 'Kashid Beach', 18.437, 72.904), ('10-korlai-beach-30-x-20', 'Korlai', 18.527, 72.917),
 ('11-revdanda-30-x-20', 'Revdanda', 18.551, 72.927), ('12-birla-mandir-30-x-20', 'Birla Mandir, Salav', 18.533, 72.948),
 ('13-sagargad-30-x-20', 'Sagargad', 18.618, 72.938), ('14-phansad-30-x-20', 'Phansad Sanctuary', 18.420, 72.960),
 ('15-magnetic-obv-30-x-20', 'Magnetic Observatory, Alibaug', 18.646, 72.876), ('16-kondana-30-x-20', 'Kondana Caves', 18.835, 73.385),
 ('17-morbe-dam-30-x-20', 'Morbe Dam', 18.983, 73.233), ('18-nandgaon-temple-30-x-20', 'Nandgaon Temple', 18.383, 72.927),
 ('19-raigad-30-x-20', 'Raigad Fort', 18.234, 73.440), ('20-raigad-30-x-20', 'Raigad Fort, ramparts', 18.231, 73.444),
 ('21-mahad-ganpati-30-x-20', 'Varadvinayak, Mahad', 18.083, 73.420), ('22-pali-ganpati-30-x-20', 'Ballaleshwar, Pali', 18.542, 73.219),
 ('23-matheran-30-x-20', 'Matheran', 18.986, 73.271), ('24-diveaagar-30-x-20', 'Diveagar', 18.172, 72.990),
 ('25-shrivardhan-30-x-20', 'Shrivardhan', 18.043, 73.016), ('26-harihareshvar-30-x-20', 'Harihareshwar', 17.996, 73.024),
 ('27-lingana-30-x-20', 'Lingana', 18.159, 73.548), ('28-mandava-30-x-20', 'Mandwa', 18.806, 72.882),
 ('29-tamhini-ghat-30-x-20', 'Tamhini Ghat', 18.454, 73.418), ('30-sarasgad-30-x-20', 'Sarasgad', 18.553, 73.236),
]

def item(folder, name, title, group, **extra):
    r = M[(folder, name)]
    return dict(title=title, group=group, sm=r['sm_path'], lg=r['lg_path'], w=r['lg_w'], h=r['lg_h'], **extra)

out = {}
for page, (folder, groups) in PAGES.items():
    out[page] = [item(folder, n, t, g) for g, items in groups for n, t in items]
out['photography'] = [item('jpeg', n, t, 'Raigad', lat=la, lon=lo) for n, t, la, lo in RAIGAD]

(ROOT / 'data/gallery.json').write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding='utf-8')
print({k: len(v) for k, v in out.items()})
