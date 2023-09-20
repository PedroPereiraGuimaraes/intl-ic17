# 🔎Accesible Campus 
Desenvolvimento de um dispositivo de localização indoor para implementação de campus universitário acessível para deficientes visuais

## 🔠Introdução 
O problema da acessibilidade de pessoas com deficiência visual diz respeito as dificuldades que elas tem ao se  deslocar em locais públicos, como prédios, shoppings, universidades, entre outros, devido a barreiras arquitetônicas e falta de informação. Diante disso,o objetivo deste trabalho é criar um software e um hardware para ajudar essas pessoas a se localizarem melhor dentro desses ambientes, fornecendo informações precisas sobre as rotas acessíveis, elevadores, escadas e outras instalações importantes. O sistema foi desenvolvido baseado em tecnologias de localização indoor. O objetivo final é permitir que as pessoas com deficiência possam se movimentar com mais autonomia e segurança dentro de qualquer ambiente.

## 📒Metodologías 
Assim, a partir das pesquisas e entrevistas, foram delineadas as seguintes ações:
 - Desenvolvimento de identificadores de localização predial pelo campus.
 - Desenvolvimento de um software que auxilie na localização dos indivíduos com deficiência visual nos prédios do Inatel. O desenvolvimento dos identificadores prediais é representado por um dispositivo que notifique por meio de áudio qual o prédio o aluno está e quais laboratórios existem ali. O aluno deve ter recursos para questionar qual a direção de um prédio específico. Assim, o identificador deve orientar se ele deve seguir adiante ou retornar. Para que a ação seja efetiva, deverá ser avaliada a colocação de faixas guias para pessoas cegas pelos prédios. 

## 🗺️Indoor Location 
Os identificadores de localização utilizam o módulo ```ESP8266```, o qual capta os sinais de todas as redes ao seu redor. Após essa captação os dados são tratados, separados entre os 3 sinais de RSSI mais fortes e os dados de ```MAC```, ```RSSI``` e ```BSSID``` são enviados para um banco de dados no ```FIREBASE```. Com um scrip em python esses dados são coletados, comparados com redes selecionadas que fazem parte dos prédios do ```INATEL``` e é feita a triangulação com esses dados de ```RSSI``` e ```MAC``` retornado as posições ```X``` e ```Y``` do módulo ```ESP8266```.

## ✅Conclusão 
Como trabalho futuro, está previsto avaliar o uso de outras tecnologias para a medida da distância, além de encontrar a melhor forma de implementar um hardware com áudio para aprimorar o protótipo. Também serão incluídas novas tecnologias para o desenvolvimento do aplicativo do projeto, visando uma melhoria contínua na experiência dos usuários. É importante destacar que iniciativas como essa são fundamentais para garantir a inclusão e acessibilidade das pessoas com deficiência visual em diferentes contextos, seja no âmbito acadêmico ou social.
