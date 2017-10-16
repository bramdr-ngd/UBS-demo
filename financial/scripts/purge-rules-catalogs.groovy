import com.ngdata.lily.dna.entitytype.DnaEntityType
import com.ngdata.lily.util.LilyConfiguration
import com.ngdata.lily.serviceregistry.local.LocalServiceRegistry
import com.ngdata.lily.multitenancy.Tenant
import com.ngdata.lily.rulesengine.RulesCatalogService

def dnaEntityType = DnaEntityType.forName("CUSTOMER")
def conf = LilyConfiguration.create()

def tenant = Tenant.fromString("0:default")
def serviceRegistry = LocalServiceRegistry.create(conf).scopeTo(tenant)
def rulesCatalogService = serviceRegistry.getService(RulesCatalogService.class)

rulesCatalogService.listCatalogs(dnaEntityType).each {
    rulesCatalogService.deleteCatalog(dnaEntityType, it.getCatalogId())
}