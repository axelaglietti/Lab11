from database.DB_connect import DBConnect
from model.product import Product
from model.sales import Vendita


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllColori():
        cnn = DBConnect.get_connection()
        result = []
        cursor = cnn.cursor(dictionary=True)
        query = """SELECT DISTINCT gp.Product_color as color
                    FROM go_products gp"""
        cursor.execute(query)
        for row in cursor:
            result.append(row["color"])
        cursor.close()
        cnn.close()
        return result

    @staticmethod
    def getProducts(colore):
        cnn = DBConnect.get_connection()
        result = []
        cursor = cnn.cursor(dictionary=True)
        query = """select *
                from go_products gp 
                where gp.Product_color = %s"""
        cursor.execute(query, (colore,))
        for row in cursor:
            result.append(Product(**row))
        cursor.close()
        cnn.close()
        return result

    @staticmethod
    def getSales(anno):
        cnn = DBConnect.get_connection()
        result = []
        cursor = cnn.cursor(dictionary=True)
        query = """select gds.*
                    from go_daily_sales gds 
                    where year(gds.`Date`) = %s"""
        cursor.execute(query, (anno,))
        for row in cursor:
            result.append(Vendita(**row))
        cursor.close()
        cnn.close()
        return result

    @staticmethod
    def getSalesSpec(v1, v2, anno):
        cnn = DBConnect.get_connection()
        cursor = cnn.cursor(dictionary=True)
        query = """select COUNT(DISTINCT gds2.`Date`) AS PESO
                    from go_daily_sales gds, go_daily_sales gds2 
                    where gds.Retailer_code = gds2.Retailer_code AND year(gds.`Date`) = %s and gds.`Date` = gds2.`Date` 
                    and gds.Product_number = %s and gds2.Product_number = %s
                """
        cursor.execute(query, (anno, v1.Product_number, v2.Product_number))
        for row in cursor:
            result = row["PESO"]
        cursor.close()
        cnn.close()
        return result
