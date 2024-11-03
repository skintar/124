game_world = {
    "портленд": {
        "name": "Портленд - Приморский город",
        "description": "Соленый бриз ласкает лицо, чайки кричат над головой, а в воздухе витает запах рыбы, рома и далеких странствий. Портленд – город моряков, торговцев и искателей приключений. Разноцветные вывески таверн манят путников отдохнуть после долгой дороги, а на оживленном рынке можно найти все, что душе угодно: от экзотических фруктов и специй до карт сокровищ и магических амулетов.",
        "sublocations": {
            "таверна": {
                "name": "«Старый парус» — Таверна у моря",
                "description": "Дым от трубок висит в воздухе, смешиваясь с ароматом пряного эля и жареного мяса. Моряки рассказывают небылицы, купцы обсуждают сделки, а искатели приключений ищут компаньонов. За стойкой, вытирая кружки, вас приветствует добродушный хозяин – одноглазый капитан в отставке.",
                "available_actions": ["выпить эля", "поговорить с хозяином", "сыграть в кости", "послушать истории"],
                "connections": {"рынок": "рынок"}
            },
            "рынок": {
                "name": "Городской рынок",
                "description": "Шумный и яркий рынок, где можно найти все, что душе угодно: от экзотических фруктов и специй до оружия и магических артефактов. Торговцы зазывают покупателей, дети играют в догонялки, а карманники ищут легкую добычу. Будьте бдительны!",
                "available_actions": ["купить зелье", "купить меч", "поторговаться", "украсть кошелек"],
                "connections": {"таверна": "таверна", "ворота": "ворота"}
            },
            "ворота": {
                "name": "Городские ворота",
                "description": "Массивные дубовые ворота, окованные железом, охраняют вход в Портленд.  Стражники зорко следят за каждым проходящим, проверяя документы и допрашивая подозрительных личностей.  За воротами простирается бескрайний мир, полный опасностей и приключений.",
                "available_actions": ["поговорить со стражником", "дать взятку"],
                "connections": {"рынок": "рынок"}
            }
        },
        "connections": {"темный_лес": "темный_лес"}
    },

    "темный_лес": {
        "name": "Темный лес",
        "description": "Древние деревья сплетаются ветвями, образуя живой туннель, сквозь который едва пробиваются лучи солнца.  Полумрак, сырость и запах прелой листвы создают гнетущую атмосферу.  Здесь легко заблудиться,  а  шорохи  в  кустах  могут  означать  встречу  с  недружелюбными  обитателями  леса.",
        "sublocations": {
            "поляна_друидов": {
                "name": "Поляна друидов",
                "description": "Круглая поляна, залитая мягким светом, посреди которой стоит древний дуб.  Воздух здесь чист и свеж,  наполнен ароматом трав и цветов.  Кажется,  что  сама  природа  охраняет  это  место.",
                "available_actions": ["поговорить с друидом",  "медитировать"],
                "connections": {"логово_волков": "логово_волков"}
            },
            "логово_волков": {
                "name": "Логово волков",
                "description": "Темная чаща,  где  земля  усыпана  костями.  Воздух  наполнен  звериным  запахом.  Вокруг  видны  следы  волков,  а  из  глубины  леса  доносятся  их  голоса.",
                "available_actions": ["атаковать волков", "спрятаться"],
                "connections": {"поляна_друидов": "поляна_друидов"}
            }
        },
        "connections": {"портленд": "портленд", "заснеженные_горы": "заснеженные_горы"}

    },


    "заснеженные_горы": {
        "name": "Заснеженные горы",
        "description": "Вершины гор, покрытые вечными снегами, упираются в небо.  Ледяной ветер  пронизывает  до  костей,  а  под  ногами  хрустит  снег.  Здесь  царит  тишина  и  покой,  нарушаемый  лишь  свистом  ветра  и  криками  горных  птиц.",
        "sublocations": {
            "горный_перевал": {
                "name": "Горный перевал",
                "description": "Узкий  перевал,  пролегающий  между  двумя  горными  пиками.  Ветер  здесь  особенно  сильный,  а  вид  с  перевала  захватывает  дух.",
                "available_actions": ["перейти перевал",  "разбить лагерь"],
                "connections": {"ледяная_пещера": "ледяная_пещера"}
            },
            "ледяная_пещера": {
                "name": "Ледяная пещера",
                "description": "Стены  и  потолок  пещеры  покрыты  льдом,  который  переливается  всеми  цветами  радуги.  В  глубине  пещеры  слышен  звук  капающей  воды.",
                "available_actions": ["исследовать пещеру", "добыть лед"],
                 "connections": {"горный_перевал": "горный_перевал"}
            }
        },
        "connections": {"темный_лес": "темный_лес", "пустыня": "пустыня"}

    },


    "пустыня": {
        "name": "Безжалостная пустыня",
        "description": "Бескрайние  пески,  раскаленные  солнцем,  простираются  до  горизонта.  Воздух  дрожит  от  жары,  а  на  небе  ни  облачка.  Здесь  выживают  только  самые  стойкие.",
        "sublocations": {
            "оазис": {
                "name": "Оазис",
                "description": "Зеленый  островок  посреди  безжизненной  пустыни.  Прохладная  вода  и  тень  пальм  дают  путешественникам  долгожданный  отдых.",
                "available_actions": ["напиться воды", "отдохнуть"],
                "connections": {"затерянный_храм": "затерянный_храм"}

            },
            "затерянный_храм": {
                "name": "Затерянный храм",
                "description": "Полуразрушенный  храм,  почти  полностью  занесенный  песком.  Стены  храма  покрыты  древними  иероглифами,  а  в  воздухе  чувствуется  атмосфера  тайны.",
                "available_actions": ["исследовать храм",  "расшифровать иероглифы"],
                "connections": {"оазис": "оазис"}

            }
        },
         "connections": {"заснеженные_горы": "заснеженные_горы", "древние_руины": "древние_руины"}

    },
    "древние_руины": {
        "name": "Древние руины",
        "description": "Разрушенные стены древнего города, хранящие множество тайн.  Время  и  стихии  сделали  свое  дело,  но  даже  в  руинах  можно  увидеть  былое  величие  этого  места.",
        "sublocations": {
            "главная_площадь": {
                "name": "Главная площадь",
                "description": "Когда-то  здесь  кипела  жизнь,  но  теперь  только  камни  молчаливо  взирают  на  проходящих.  Посреди  площади  стоит  фонтан,  вода  в  котором  давно  высохла.",
                "available_actions": ["исследовать площадь",  "искать артефакты"],
                "connections": {"подземелье": "подземелье"}

            },
            "подземелье": {
                "name": "Подземелье",
                "description": "Темное  и  сырое  подземелье,  где  легко  заблудиться.  В  воздухе  пахнет  плесенью  и  сыростью,  а  из  глубины  доносятся  странные  звуки.",
                "available_actions": ["исследовать подземелье",  "сражаться с крысами"],
                "connections": {"главная_площадь": "главная_площадь"}
            }
        },
        "connections": {"пустыня": "пустыня"}
    }
}