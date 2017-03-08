select t1.usr,t1.ee_cnt, t2.er_cnt, nvl(t3.tw_cnt,0) as tw_cnt,nvl(t4.tid,''),nvl(t4.text,''),nvl(t5.tdate,''),nvl(t5.tid,''),nvl(t5.text,''),nvl(t5.tdate,'')
From ((((select u1.usr,count(ee.flwee) as ee_cnt
        From (users u1 full outer join follows ee on ee.flwer = u1.usr)
        group by u1.usr) t1
        full outer join 
        (select u2.usr,count(er.flwee) as er_cnt
        From (users u2 full outer join follows er on er.flwee = u2.usr)
        group by u2.usr) t2
        on t1.usr = t2.usr)
        full outer join
        (select tw1.writer,tw1.tid, count(Distinct tw1.tid) as tw_cnt
        From tweets tw1
        group by tw1.writer,tw1.tid) t3
        on t3.writer = t1.usr)
        full outer join 
        (select*
        From (select tw2.writer,tw2.tid,tw2.text,tw2.tdate,row_number() over(partition by tw2.writer order by tw2.tdate) row_number
                From tweets tw2) 
                WHERE row_number<=3)t4
        on t4.writer = t1.usr)
        full outer join
        (select tw2.writer,tw2.tid,tw2.text,tw2.tdate
        From tweets tw2)t5
        on t5.writer = t1.usr
order by t1.usr DESc;


