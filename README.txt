Civil defense
Проектная группа: Белякова Анна

Версия питона: python 3.9

Управление: правая кнопка мыши - выстрел из оружия (если оно есть).
Английская "p" - в домашней сцене - купить персонажа, поменять персонажа;
на уровнях - открыть сундук, взять его содержимое.

Идея игры:
пиксельная игра.
Игрок выбирает персонажа и попадает на первый уровень, состоящий из нескольких комнат.
В комнатах рандомно расположены: ящики с оружием или зельями жизни и энергии, враги.
Цель игрока - найти в одной из комнат портал и с его помощью перейти на следующий уровень.
Пока игрок ищет портал, он будет с помощью оружия убивать врагов. Следующий уровень
генерируется так же - комнаты случайно наполняются объектами: оружием, врагами,
порталом. Уровни можно проходить бесконечно долго.

Характеристики персонажа, за которого играет user:
во время прохождений уровней пользователь видит свои данные: количество жизней,
количество энергии. Пользователя могут атаковать враги, тогда
характеристики юзера будут ухудшаться. Когда количество жизней = 0, пользователь
заканчивает сеанс окном с результатами и возвращается на "домашнюю карту", где
снова может поменять скин.

Общая информация об игре:
в интересах пользователя пройти как можно больше уровней подряд, чтобы заработать как
можно больше монет, на которые он сможет купить себе другого персонажа.
