import mysql.connector

class Database:
    def __init__(self):
        self.db=None

    def ulanish(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="diyorbek1122",
            database="food_servise",
            port="3308"
        )

    def ishlatish(self,sql,fetchall=False, fetchone=False, commit=False):
        self.db=self.ulanish()
        cursor=self.db.cursor()
        cursor.execute(sql)
        data=None
        if fetchall:
            data = cursor.fetchall()
        elif fetchone:
            data= cursor.fetchone()
        elif commit:
            self.db.commit()
        self.db.close()
        return data
    def foodlist(self):
        sql=f"select * from food "
        return self.ishlatish(sql,fetchall=True)
    def foodprice(self,id):
        sql = "select min(narxi) , max(narxi) from ovqat miqdorlari where ovqat_id={id}"
        return self.ishlatish(sql , fetchone=True)
    def menudetail(self , id ):
        sql = f"""
              SELECT ovqat_miqdorlari.narxi, 
                     ovqat_miqdorlari.tarifi, 
                     ovqat_miqdorlari.rasmi,
                    miqdor.turi,
                    ovqat_miqdorlari.id
                FROM miqdor INNER JOIN ovqat_miqdorlari 
                ON miqdor.id = ovqat_miqdorlari.miqdor_id
                where ovqat_miqdorlari.ovqat_id={id}
                """
        return self.ishlatish(sql , fetchall=True)

    def savatcha(self ):
        sql="""
    SELECT food.nomi,
            ovqat_miqdorlari.narxi, 
           ovqat_miqdorlari.tarifi, 
           ovqat_miqdorlari.rasmi,
           miqdor.turi,
           savatcha.soni
    FROM miqdor
    INNER JOIN ovqat_miqdorlari ON miqdor.id = ovqat_miqdorlari.miqdor_id
    INNER JOIN savatcha ON ovqat_miqdorlari.id = savatcha.ovqat_id
    INNER JOIN food ON ovqat_miqdorlari.ovqat_id = food.id
    where savatcha.user_id = {id}
    """
        return self.ishlatish(sql  , fetchall=True)
    def registratsiya(self , ism , familiya , login , pasword):
        sql = f"""
                insert into foydalanuvchilar(ism , familiya , login  ,parol)
                values('{ism}' ,'{familiya}' ,'{login}' , '{pasword}')
                """
        self.ishlatish(sql , commit=True)
    def check_user(self , login ,parol):
        sql = f"""
                    SELECT * FROM foydalanuvchilar WHERE login = '{login}' and parol = '{parol}'
                """
        return self.ishlatish(sql, fetchone=True)
    def user_savat(self , id):
        sql = f"""

       SELECT food.nomi,
            ovqat_miqdorlari.narxi, 
            ovqat_miqdorlari.tarifi, 
            ovqat_miqdorlari.rasmi,
            miqdor.turi,
            savatcha.soni,
            savatcha.id
        FROM miqdor
        INNER JOIN ovqat_miqdorlari ON miqdor.id = ovqat_miqdorlari.miqdor_id
        INNER JOIN savatcha ON ovqat_miqdorlari.id = savatcha.ovqat_id
        INNER JOIN food ON ovqat_miqdorlari.ovqat_id = food.id
        where savatcha.user_id={id}
        """
        return self.ishlatish(sql , fetchall=True)
    def delmahsulot(self , id):
        sql = f" delete from savatcha where id={id}"
        self.ishlatish(sql , commit=True)
    def addsavat(self , userid , ovqatid ,zakazid ,  soni):
        sql = f"""INSERT INTO savatcha(user_id , ovqat_id , zakaz_id , soni)
        VALUES ('{userid}' , '{ovqatid}' ,'{zakazid}', {soni})"""
        self.ishlatish(sql , commit=True)
obj=Database()
