*emotional-status*
[:love :love :love]

(with-fast-forward {:weeks 4}
  *emotional-status*)
[:down :down :down]

(describe partner)
{:height :tall,
 :weight (not :much),
 :smell :fresh-avocado}

(describe (:laughter partner))
(when (stepping-on
       (bag-of potato-chips))
  (make-sound :jiggling))

(assume
 (count
  (lovers partner)))
1

(assume
  (-> (lovers partner)
      (except :me)))
nil

(count (lovers partner))
2

(def the-other 
  (-> (lovers partner)
      (except :me)))

(describe the-other)
nil

(with-nickname 
  (describe the-other))
{:name :potato-head}

(find-out-name the-other)
<MissingArgumentException: "common-friend argument not given">

(find-out-name the-other partner)
"A...es" ; Data omitted for privacy reasons 

(def potato-head-address (find-out-address the-other))

(describe car)
{:color #000000, ;black
 :manufacturer :volvo,
 :year 2020}

(contains? car :leather-seat)
true

(contains? car :remote-start)
false

(with-timer
  (drive-to potato-head-address))
{:hours 0, :minutes 13, :seconds 37}

(with-timer
  (enter-property (:backyard potato-head-address)))
{:hours 0, :minutes 0, :seconds 22}

(locate the-other)
{:location :yoga-mat,
 :activity :fuck-knows-asana}

(locate :heavy-object)
{:location (next-to :yoga-mat),
 :material (assume :brass),
 :type :sound-bowl}

(with-timer 
  (and
    (grab :sound-bowl)
    (hit the-other :sound-bowl)
    (drop :sound-bowl)))
{:hours 0, :minutes 0, :seconds 0}

*emotional-status*
[:powerful :satisfied :confused]

(with-fast-forward {minutes 2}
  *emotional-status)
[:omg]

(analyze-fluid (look-down))
{:color #FF0000 ; red
 :material :blood}

(dial 911)
; ...

(with-fast-forward {:days 1}
  (locate :me))
{:location :county-jail,
 :activity nil}
