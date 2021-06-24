class CircleGraph extends Graph{
    constructor(config) {
        super(config);

        this.dom_object = $("<div/>", {
            "id": this.config.uid + "_graph",
            "class": 'col'
        });

        let card = $("<div/>", {"class": "card"});
        let header = $("<div/>", {"class": "card-header"});
        let body = $("<div/>", {"class": "card-body"});

        let title = $("<span/>", {
            "id": this.config.uid + "_title",
            "text": this.config.title
        });

        let circle = $("<div/>", {
            "id": this.config.uid + "_circle",
            "class": 'c100 p0 med orange center',
            "data-placement": "bottom",
            "title": "..."
        }).append(
            $("<span/>", {
                "id": this.config.uid + "_parent"
            }).append(
                $("<span/>", {
                    "id": this.config.uid + "_level"
                }).append(
                    $("<i/>", {
                        "class": "fa fa-fw fa-ellipsis-h"
                    })
                ),
                $("<span/>", {
                    "id": this.config.uid + "_unit",
                    "style": this.config.unit_style
                }),
            ),
            $("<div/>", {
                "class": 'slice'
            }).append(
                $("<div/>", {
                    "id": this.config.uid + "_bar",
                    "class": 'bar'
                }),
                $("<div/>", {
                    "id": this.config.uid + "_fill",
                    "class": 'fill'
                })
            )
        );

        header.append(title);
        body.append(circle);
        card.append(body, header);
        this.dom_object.append(card);
    }

    appendTo(target) {
        super.appendTo(target);
        let id = "#" + this.config.uid + "_circle";
        // Enable tooltips
        $(id).tooltip({
            trigger: "hover"
        });
    }

    setup(index, data, name) {
        // Get maximum from the initial message
        this.config.limit = data["limit"];
        // Set theme accent colour from config
        let accent_colour = loadConfigSetting(['interface', 'theme', 'accent_colour'], '#FF5A00');
        $('#' + this.config.uid + "_bar").css("border-color", accent_colour);
        $('#' + this.config.uid + "_fill").css("border-color", accent_colour);
    }


    update(index, data, name) {
        // Maximum value of graph. Use the user's value if set, otherwise the value provided by sensor itself, else 100.
        let max = this.config.maximum || this.config.limit;
        if (!max) {
            max = 100;
            interfaceLog("warning", "sensors", "Sensor " + name + " is not providing" +
                " a maximum value. You should set this in your " + this.config.uid + " graph config instead. Default " +
                "of 100 is used.")
        }
        let level = $("#" + this.config.uid + "_level");
        let unit_text = $("#" + this.config.uid + "_unit");
        let circle = $("#" + this.config.uid + "_circle");
        let unit = this.config.unit;
        level.html(data);
        unit_text.html(unit);
        let percent = Math.round((data / max) * 100);
        if (percent > 100) percent = 100;
        circle.attr('class', "c100 med orange center p" + percent);
        circle.attr('data-original-title', data + " / " + max + " " + unit);
    }
}

