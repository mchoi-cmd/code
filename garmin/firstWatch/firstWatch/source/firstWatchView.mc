import Toybox.Graphics;
import Toybox.Lang;
import Toybox.System;
import Toybox.WatchUi;
import Toybox.Time;

class firstWatchView extends WatchUi.WatchFace {

    function initialize() {
        WatchFace.initialize();
    }

    // Load your resources here
    function onLayout(dc as Dc) as Void {
        setLayout(Rez.Layouts.WatchFace(dc));
    }

    // Called when this View is brought to the foreground. Restore
    // the state of this View and prepare it to be shown. This includes
    // loading resources into memory.
    function onShow() as Void {
    }

    // Update the view
    function onUpdate(dc as Dc) as Void {
        setTimeLabel();
        setBatteryLabel();
        setDateLabel();
        test();
        //useGraphic(dc);
        // Call the parent onUpdate function to redraw the layout
        //  dc.drawRadialText(x, y, font, text, justification, angle, radius, direction)

        View.onUpdate(dc);
        useGraphic(dc);
    }

    function test(){



        // Get and show the current time
        var clockTime = System.getClockTime();
        var timeString = Lang.format("$1$:$2$:$3$", [clockTime.hour.format("%02d"), clockTime.min.format("%02d"), clockTime.sec.format("%02d")]);
        var view = View.findDrawableById("RadLabel") as Text;

        view.setText(timeString);
    }

    function useGraphic(dc as Dc){
        // dc.setColor(Graphics.COLOR_RED, Graphics.COLOR_BLACK);
        // dc.fillCircle(50, 100, 75);


        var sampleFont = Graphics.getVectorFont({:face=>["RobotoRegular","Swiss721Regular"], :size=>16});
        if (sampleFont != null)
        {
            dc.drawRadialText(
                dc.getWidth() / 2,
                dc.getHeight() / 2,
                sampleFont,
                "test this very long string so I can see if this rotates ddd ddd ddd ddd ddddffdfdafda",
                Graphics.TEXT_JUSTIFY_CENTER,
                60,
                200,
                Graphics.RADIAL_TEXT_DIRECTION_CLOCKWISE);
        }


        // dc.drawText(
        //     dc.getWidth() / 2,                      // gets the width of the device and divides by 2
        //     dc.getHeight() / 2,                     // gets the height of the device and divides by 2
        //     Graphics.FONT_LARGE,                    // sets the font size
        //     "Hello World",                          // the String to display
        //     Graphics.TEXT_JUSTIFY_CENTER            // sets the justification for the text
        // );


    }


    function setTimeLabel(){
        // Get and show the current time
        var clockTime = System.getClockTime();
        var timeString = Lang.format("$1$:$2$:$3$", [clockTime.hour.format("%02d"), clockTime.min.format("%02d"), clockTime.sec.format("%02d")]);
        var view = View.findDrawableById("TimeLabel") as Text;

        view.setText(timeString);
    }

    function setBatteryLabel() {
    	var battery = System.getSystemStats().battery;
        var batteryString = Lang.format("$1$", [battery.format("%01d")]);


        var batteryDisplay = View.findDrawableById("BatteryLabel") as Text;
        batteryDisplay.setText(batteryString);
    }

    function setDateLabel() {
    	var date = Gregorian.info(Time.now(), Time.FORMAT_MEDIUM);
        var dateString = Lang.format("$1$ $2$ $3$", [date.day_of_week, date.month, date.day]);


        var dateDisplay = View.findDrawableById("DateLabel") as Text;
        dateDisplay.setText(dateString);
    }

    // Called when this View is removed from the screen. Save the
    // state of this View here. This includes freeing resources from
    // memory.
    function onHide() as Void {
    }

    // The user has just looked at their watch. Timers and animations may be started here.
    function onExitSleep() as Void {
    }

    // Terminate any active timers and prepare for slow updates.
    function onEnterSleep() as Void {
    }

}
