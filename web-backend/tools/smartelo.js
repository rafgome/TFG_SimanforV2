const XlsxPopulate = require("xlsx-populate");
const templateURL = `${__dirname}/../input/smartelo_template.xlsm`;

const arbolesMap = {
  'Arbol': 3,
  'Cuadrante': 2,
  'Estaca referencia': '',
  'Azimut': '',
  'Distancia': '',
  'Especie': 4,
  'Diam1': '',
  'Diam2': '',
  'Ht(m)': 13,
  'Hcv(m)': 12,
  'A': 33,
  'B': 34,
  'C': 35,
  'D': 36,
  'Volumen': 17,
  'Muerto': '',
  'Riesgo depreciación': 37,
  'Defectos copa': 38,
  'Estado': '',
  'Códigos ecológicos': 39,
  'CoordX': 6,
  'CoordY': 7,
  'Crecimiento diametral': 31,
  'Crecimiento volumen': 32,
  'Diam': 11,
  'CD': '',
  'Área normal': '',
  'Volumen | Volumen tarifas': '',
  'Calidad': 16,
};

const reasonMap = {
  "dead": "Muerto",
  "exploitation": "Explotación",
  "forked": "Bifurcado",
  "fallen": "Caído",
  "trunked": "Tronchado",
  "crooked": "Torcido",
  "substitution": "Sustitución",
  "sick": "Enfermo",
  "submerged": "Sumergido",
  "future": "Porvenir",
  "biodiversity": "Biodiversidad",
  "protected": "Protegido",
  "other": "Otra"
};

const actionsMap = {
  "cut": "Cortar",
  "preserve": "Preservar"
}

const industriasMap = {
  'Vsc;Vfuste (m3)': 24,
  'Vtrit (m3)': 30,
  'Vapea (m3)': 29,
  'Vcanter (m3)': 28,
  'Vsierra (m3)': 27,
  'Vsgruesa (m3)': 26,
  'Vchapa (m3)': 25
};

const biomasaMap = { 
  'B_PM (t)': 18,
  'B_R>7 (t)': 19,
  'B_2-7 (t)': 20,
  'B_R<2 (t)': 21,
  'B_Raíz (t)': 22
};

const readTemplate = async () => {
  return XlsxPopulate.fromFileAsync(templateURL);
}

function insertInicio(inventory, smartelo){
  // Insert 'Area de Señalamiento' field
  smartelo.cell('C5').value(inventory[1]);
  // Insert 'Parcela' field
  smartelo.cell('C6').value(inventory[2]);
  // Insert 'Superficie' field (ha)
  smartelo.cell('C7').value(inventory[3]/10000);
}

function insertCoordenadas(inventory, smartelo){
  const dest = [];
  for (const row of inventory) {
      const newRow = [];
      if (row[arbolesMap['Especie']] == 'estaca'){
          newRow.push(parseInt(row[arbolesMap['Arbol']]));
          newRow.push('', '', '', '');
          newRow.push('', '', '');
          newRow.push(parseFloat(row[arbolesMap['CoordX']]));
          newRow.push(parseFloat(row[arbolesMap['CoordY']]));
          dest.push(newRow);
      }
  }
  smartelo.cell("B5").value(dest);
}

function insertArboles(inventory, smartelo){
  const dest = [];      
  for (const row of inventory) {
      if (row[arbolesMap['Especie']] == 'estaca'){
          continue;
      }
      const newRow = [];
      for (const key in arbolesMap) {
          if (!isNaN(parseFloat(row[arbolesMap[key]]))){
              row[arbolesMap[key]] = parseFloat(row[arbolesMap[key]]);
              if (key == 'Volumen'){
                  row[arbolesMap[key]] = row[arbolesMap[key]]/1000;
              }
          }
          newRow.push(row[arbolesMap[key]]);
      }
      dest.push(newRow);
  }

  smartelo.cell("B2").value(dest);
}

function insertEquipos(user, actions, smartelo){
  const dest = [];
  actions = actions.sort((a, b) => a['action'].localeCompare(b['action']));
  for (const item of actions){
        dest.push([
          user,
          parseInt(item.tree_id),
          actionsMap[item.action],
          reasonMap[item.reason] !== undefined ? reasonMap[item.reason] : "-"]);
  }
  smartelo.cell("B5").value(dest);
}

function insertIndustrias(inventory, smartelo){
  const dest = [];      
  for (const row of inventory) {
      const newRow = [];
      for (const key in industriasMap) {
          if (!isNaN(parseFloat(row[industriasMap[key]]))){
              row[industriasMap[key]] = parseFloat(row[industriasMap[key]]);
          }
          newRow.push(row[industriasMap[key]]);
      }
      dest.push(newRow);
  }

  smartelo.cell("F5").value(dest);
}

function insertBiomasa(inventory, smartelo){
  const dest = [];
  for (const row of inventory) {
      const newRow = [];
      for (const key in biomasaMap) {
          if (!isNaN(parseFloat(row[biomasaMap[key]]))){
              row[biomasaMap[key]] = parseFloat(row[biomasaMap[key]]);
          }
          newRow.push(row[biomasaMap[key]]);
      }
      dest.push(newRow);
  }
  smartelo.cell("E5").value(dest);
}

module.exports = {
  insertArboles,
  insertBiomasa,
  insertCoordenadas,
  insertEquipos,
  insertIndustrias,
  insertInicio,
  readTemplate
};
